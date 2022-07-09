# NavVisualSemanticMemory

#### Abstract:
Navigation is an important activity to be performed by mobile robots with high complexity in the context of indoor environments. Approaches as Deep Reinforcement Learning has been adopted for this purpose, from the premise of learning through experiences and taking advantage of Deep Neural Networks as Convolutional Networks, Graph Neural Networks, and Recurrent Networks. Based on the use of vision and semantic context applied in this work, the effects of adding Recurrent Networks on a learning-based navigation model are investigated, making possible the learning of better policies with the use of memory from past experiences.  Results obtained show that the proposed approach gets better values in terms of qualitative as quantitative measures when compared to models without memory.

By Iury Santos and Roseli Romero

Presented at 17th IEEE Latin American Robotics Symposium - LARS 2020

[Paper Link - Open Reading Access](https://rdcu.be/cHIJZ) 

[Video](https://youtu.be/1hDLtMXapbg)


## Results

|          	| All               	| All              	| L ≥ 5           	| L ≥ 5            	|
|----------	|-------------------	|------------------	|-----------------	|------------------	|
| Model    	| **STT**           	| **TS**           	| **STT**         	| **TS**           	|
| Random   	| 4.35              	| 10.20            	| 0.03            	| 0.18             	|
| A3C      	| 6.38 ±(0.25)      	| 14.76 ±(1.32)    	| 0.06 ±(0.22)    	| 1.94 ±(0.77)     	|
| GCN-MLP  	| 7.29 ±(0.42)      	| 15.38 ±(0.73)    	| 1.68 ±(0.17)    	| 3.95 ±(0.17)     	|
| GCN-GRU  	| 8.16 ±(1.20)      	| 18.64 ±(4.88)    	| 3.08 ±(1.57)    	| 6.10 ±(3.51)     	|
| GCN-LSTM 	| **11.62** ±(0.88) 	| **26.32**±(2.18) 	| **6.84**±(1.38) 	| **12.93**±(2.75) 	|


## Setup

1. Install the requirements listed in ``requirements.txt``. If you use pip, run ``pip install -r requirements.txt``
2. Download the [data](https://prior-datasets.s3.us-east-2.amazonaws.com/savn/data.tar.gz) in the project directory. Unrar with:

    ``tar -xzf data.tar.gz``

- Those folders contains the ``thor_offiline_data`` to offline training in the environment AI2-THOR. 
- The ``thor_glove`` with GloVe embeddings for the objects in the ambiance.
- The ``GCN`` containing the data for the Graph Convolutional Neural Network used by GCN-MLP, GCN-GRU and GCN-LSTM models.

The original version of this code is available at [SAVN](https://github.com/allenai/savn) repository (with the data also linked in the above links), which has been modifield for our project with the addition and evaluations of memory mechanisms like LSTM and GRU networks.

### Pretrained models with our results
The pretrained models of our work for GCN-MLP, GCN-GRU and GCN-LSTM can be downloaded [here](https://drive.google.com/drive/folders/1uHMkef1BjHYi3cQarWkHnpikJIjwydcg?usp=sharing).

## Running

For run our pretrained models in evaluation mode. In the example bellow, to run the GCN-LSTM with pretained model:
    
    python main.py --eval \
        --test_or_val test \
        --episode_type TestValEpisode \
        --load_model trained_models/gcn_lstm_model.dat \
        --model GCN \
        --results_json gcn_lstm.json 

To run the GCN-GRU with pretained model:

    python main.py --eval \
        --test_or_val test \
        --episode_type TestValEpisode \
        --load_model trained_models/gcn_gru_model.dat \
        --model GCN_GRU \
        --results_json gcn_gru.json 


## Traning
To train a model of type GCN-LSTM:

        python main_load.py --model GCN \
            --title gcn_lstm \
            --gpu-ids 0 1 \
            --workers 8


To train a model of type GCN-MLP:

        python main_load.py --model GCN_MLP \
            --title gcn_mlp \
            --gpu-ids 0 1 \
            --workers 8

## Citation

    @inproceedings{santoseromero2020,
	title={Deep Reinforcement Learning for Visual Semantic Navigation with Memory},
	author={Santos, Iury and Romero, Roseli},
	booktitle={Proceedings of the IEEE Latin American Robotics Symposium / Brazilian Symposium of Robotics},
	pages={1--6},
	year={2020}}
