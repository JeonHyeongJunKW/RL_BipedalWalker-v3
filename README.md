# RL_BipedalWalker-v3
Bipedal walker의 3버전의 코드를 구현합니다.

### 액션종류 
example) 
```
[-0.13214321  0.5659649   0.87031937  0.72357774]
```
### 리턴값

example) 
```
(array([-0.02106741, -0.03130611, -0.02870544, -0.01356055,  0.47751102,
        0.9997741 ,  0.0709933 , -1.0005901 ,  1.        ,  0.37933013,
        0.9994029 ,  0.07580382, -1.0004629 ,  1.        ,  0.44617477,
        0.45124176,  0.46703416,  0.49550363,  0.54059803,  0.6097876 ,
        0.7177729 ,  0.8967057 ,  1.        ,  1.        ], dtype=float32), -0.21231491802136224, False, {})
```

### Dependencies
아래의 명령어를 수행하여 의존성있는 파일들을 설치합니다.
 파이썬 버전은 3.x 이상인지 확인합니다.
```
sudo sh setup.sh
```

### simple_render_test.py
: 2021/12/10에 간단하게 Bipedal Walker의 랜더링을 구현한것입니다.


### main_run.py
: 2021/12/11에 간단하게 Bipedal Walker에 대한 A2C 학습모델을 만든것입니다. 

### main_learning_test.ipynb
: 2021/12/12에 Bipedal Walker에 대한 하이퍼파라미터 튜닝을 위한 jupyter notebook code

### model_test.py
: 2021/12/13에 간단하게 완성된 모델입니다. 추가적인 학습이 필요합니다. 

# 모델별 성능테스트 

## 기본 optimal model
: 가장 안정적인 구동을 하지만 느리다. 한쪽 다리로 뒤로넘어지지 않도록 지지한다.

<img width = "300" src="https://user-images.githubusercontent.com/63538314/145970849-a412dc79-5eba-4127-a364-ab026964adcb.png">

## 진화단계의 optimal model
: 쓰러지지만, 점차 빠르고 좋은 보행자세와 reward를 반환하고있다.

<img width = "300" src="https://user-images.githubusercontent.com/63538314/145970746-00946014-658a-48f4-9a51-29c1e9bbc592.png">
<img width = "300" src="https://user-images.githubusercontent.com/63538314/145970221-32bbbf7a-c0d4-41ba-b8e9-815c38b5b872.png">


## Update
2021/12/13 : 모델구조 및 하이퍼파라미터 수정(학습에 사용되는 batch size 조정)
2021/12/14 : 최종학습모델 튜닝(이전과 다르게 새로운 포즈로 이동시도중)