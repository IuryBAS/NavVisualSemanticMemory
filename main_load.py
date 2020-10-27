from __future__ import print_function, division

import os
import random
import ctypes
import setproctitle
import time

import numpy as np
import torch
import torch.multiprocessing as mp
from tensorboardX import SummaryWriter

from utils import flag_parser

from utils.class_finder import model_class, agent_class, optimizer_class
from utils.net_util import ScalarMeanTracker
from main_eval import main_eval

from runners import nonadaptivea3c_train, nonadaptivea3c_val


os.environ["OMP_NUM_THREADS"] = "1"


def main():
    setproctitle.setproctitle("Train/Test Manager")
    args = flag_parser.parse_arguments()

    if args.model == "BaseModel" or args.model == "GCN_MLP" or  args.model == "GCN" or args.model == "GCN_GRU":
        args.learned_loss = False
        args.num_steps = 50
        target = nonadaptivea3c_val if args.eval else nonadaptivea3c_train
   
    create_shared_model = model_class(args.model)
    init_agent = agent_class(args.agent_type)
    optimizer_type = optimizer_class(args.optimizer)

    if args.eval:
        main_eval(args, create_shared_model, init_agent)
        return

    model_to_open = args.load_model

    if model_to_open != "":
        shared_model = create_shared_model(args)
        optimizer = optimizer_type(
                filter(lambda p: p.requires_grad, shared_model.parameters()), args
            )
        saved_state = torch.load(
            model_to_open, map_location=lambda storage, loc: storage
        )
        shared_model.load_state_dict(saved_state['model'])
        optimizer.load_state_dict(saved_state['optimizer'])
        optimizer.share_memory()
        train_total_ep = saved_state['train_total_ep']
        n_frames = saved_state['n_frames']

    else:
        shared_model = create_shared_model(args)

        train_total_ep = 0
        n_frames = 0

        if shared_model is not None:
            shared_model.share_memory()
            optimizer = optimizer_type(
                filter(lambda p: p.requires_grad, shared_model.parameters()), args
            )
            optimizer.share_memory()
            print(shared_model)
        else:
            assert (
                args.agent_type == "RandomNavigationAgent"
            ), "The model is None but agent is not random agent"
            optimizer = None

    processes = []

    end_flag = mp.Value(ctypes.c_bool, False)

    train_res_queue = mp.Queue()
    

    start_time = time.time()
    local_start_time_str = time.strftime(
        "%Y-%m-%d_%H:%M:%S", time.localtime(start_time)
    )
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    random.seed(args.seed)

    if args.log_dir is not None:
        tb_log_dir = args.log_dir + "/" + args.title + "-" + local_start_time_str
        log_writer = SummaryWriter(log_dir=tb_log_dir)
    else:
        log_writer = SummaryWriter(comment=args.title)

    if args.gpu_ids == -1:
        args.gpu_ids = [-1]
    else:
        torch.cuda.manual_seed(args.seed)
        

    
    for rank in range(0, args.workers):
        p = mp.Process(
            target=target,
            args=(
                rank,
                args,
                create_shared_model,
                shared_model,
                init_agent,
                optimizer,
                train_res_queue,
                end_flag,
            ),
        )
        p.start()
        processes.append(p)
        time.sleep(0.1)

    print("Train agents created.")

    train_thin = args.train_thin
    train_scalars = ScalarMeanTracker()

    print(train_total_ep)
    print(optimizer)
    try:
        while train_total_ep < args.max_ep:

            train_result = train_res_queue.get()
            train_scalars.add_scalars(train_result)
            train_total_ep += 1
            n_frames += train_result["ep_length"]
            if (train_total_ep % train_thin) == 0:
                log_writer.add_scalar("n_frames", n_frames, train_total_ep)
                tracked_means = train_scalars.pop_and_reset()
                for k in tracked_means:
                    log_writer.add_scalar(
                        k + "/train", tracked_means[k], train_total_ep
                    )

            if (train_total_ep % args.ep_save_freq) == 0:

                print(n_frames)
                if not os.path.exists(args.save_model_dir):
                    os.makedirs(args.save_model_dir)
                state_to_save = shared_model.state_dict()
                save_path = os.path.join(
                    args.save_model_dir,
                    "{0}_{1}_{2}_{3}.dat".format(
                        args.title, n_frames, train_total_ep, local_start_time_str
                    ),
                )
                save_dict = {'model': state_to_save, 'train_total_ep':train_total_ep, 'optimizer':optimizer.state_dict(), 'n_frames':n_frames}
                torch.save(save_dict, save_path)
                #torch.save(state_to_save, save_path)

    finally:
        log_writer.close()
        end_flag.value = True
        for p in processes:
            time.sleep(0.1)
            p.join()


if __name__ == "__main__":
    mp.set_start_method("spawn")
    main()
