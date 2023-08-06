from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout, BatchNormalization # Подлкючаем керасовский слой Dense
from tensorflow.keras.models import load_model, Sequential # Подключаем модель типа Sequential
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from tensorflow.keras.utils import to_categorical, plot_model # Полкючаем методы .to_categorical() и .plot_model()
sns.set_style('darkgrid')
from tensorflow.keras.utils import to_categorical, plot_model # Полкючаем методы .to_categorical() и .plot_model()
from tensorflow.keras import backend as K # Импортируем модуль backend keras'а
from tensorflow.keras.optimizers import Adam # Импортируем оптимизатор Adam
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import Model # Импортируем модели keras: Model
from tensorflow.keras.layers import Input, Conv2DTranspose, concatenate, Activation, MaxPooling2D, Conv2D, BatchNormalization # Импортируем стандартные слои keras
from . import сегментация
import importlib.util, sys, gdown

def создать_слой(данные, input_shape=None, last_layer=False):
  args = {'activation':'relu'}
  if input_shape != None:
    args['input_shape'] = input_shape
  if last_layer:
    args['activation'] = 'softmax'
  if '-' in данные:
    буква, параметр = данные.split('-')    
  else:
    буква = данные
  if буква == 'Д':
    return Dense(int(параметр), **args)
  if буква == 'С':
    return Conv2D(int(параметр), (3,3), padding='same', **args)
  if буква == 'Ф':
    return Flatten()
  if буква == 'Б':
    return BatchNormalization()
  if буква == 'М':
    return MaxPooling2D()    
  if буква == 'Др':
    return Dropout(float(параметр))
  
def структура_сети(модель):
  print('Структура модели:')
  print('_________________________________________________________________')
  print(модель.summary()) 
  return plot_model(модель, show_shapes=True) # Выводим схему модели

def создать_сеть(**kwargs):
  layers = kwargs['слои'].split()
  model = Sequential()
  model.add(создать_слой(layers[0], kwargs['входной_размер']))  
  for i in range(1, len(layers) -1):
    model.add(создать_слой(layers[i]))
  model.add(создать_слой(layers[-1], last_layer = True))
  print('Создана модель нейронной сети!')
  model.compile(loss='sparse_categorical_crossentropy', optimizer = 'adam', metrics =['accuracy'])
  return model


def создать_линейную_сеть(**kwargs):  
  #  Собственная функция метрики, обрабатывающая пересечение двух областей
  def точность(y_true, y_pred):
    # Возвращаем площадь пересечения деленную на площадь объединения двух областей
    return (2. * K.sum(y_true * y_pred) + 1.) / (K.sum(y_true) + K.sum(y_pred) + 1.)
  layers = kwargs['слои'].split()
  img_input = Input(kwargs['входной_размер'])
  x = создать_слой(layers[0], kwargs['входной_размер']) (img_input)
  for i in range(1, len(layers) -1):
    x = создать_слой(layers[i]) (x)
  x = создать_слой(layers[-1], last_layer = True) (x)
  мод = Model(img_input, x)
  print('Создана модель нейронной сети!')
  мод.compile(loss='categorical_crossentropy', optimizer=Adam(lr=3e-4), metrics =[точность])
  return мод

def создать_UNET(**kwargs):
  def точность(y_true, y_pred):
    return (2. * K.sum(y_true * y_pred) + 1.) / (K.sum(y_true) + K.sum(y_pred) + 1.)
  block1 = kwargs['блок_вниз'].split()
  block2 = kwargs['блок_вверх'].split()
  if 'количество_выходных_классов' in kwargs:
    n_classes = kwargs['количество_выходных_классов']
  else:
    n_classes = 2
  img_input = Input(kwargs['входной_размер'])
  b_o = []
  # DOWN
  x = создать_слой(block1[0]+'-'+str(kwargs['начальное_значение']), kwargs['входной_размер']) (img_input)
  for i in range(1, len(block1)):
    x = создать_слой(block1[i]+'-'+str(kwargs['начальное_значение'])) (x)
  b_o.append(x)
  x = MaxPooling2D()(b_o[-1])    
  for i in range(kwargs['количество_блоков']-1):
    for j in range(len(block1)):
      x = создать_слой(block1[j]+'-'+str(2**(i+1)*kwargs['начальное_значение'])) (x)
    b_o.append(x)
    x = MaxPooling2D()(b_o[-1])
  x = b_o[i+1]   
  # UP
  for i in range(kwargs['количество_блоков']-1):
    x = Conv2DTranspose(2**(2*kwargs['количество_блоков']-i), (2, 2), strides=(2, 2), padding='same')(x)    # Добавляем слой Conv2DTranspose с 256 нейронами
    for j in range(len(block2)):
      if block2[j]=='К':
        x = concatenate([x, b_o[kwargs['количество_блоков']-i-2]])
      else:
        x = создать_слой(block2[j]+'-'+str(2**(2*kwargs['количество_блоков']))) (x)
  x = Conv2D(n_classes, (3, 3), activation='softmax', padding='same')(x)  # Добавляем Conv2D-Слой с softmax-активацией на num_classes-нейронов

  мод = Model(img_input, x)

  print('Создана модель нейронной сети!')
  мод.compile(loss='categorical_crossentropy', optimizer=Adam(lr=3e-4), metrics =[точность])
  return мод

def создать_PSP(**kwargs):
  def точность(y_true, y_pred):
    return (2. * K.sum(y_true * y_pred) + 1.) / (K.sum(y_true) + K.sum(y_pred) + 1.)
  
  conv_size = kwargs['количество_фильтров']
  img_input = Input(kwargs['входной_размер'])
  nBlock = kwargs['количество_блоков']
  if 'количество_выходных_классов' in kwargs:
    n_classes = kwargs['количество_выходных_классов']
  else:
    n_classes = 2
  x = Conv2D(conv_size, (3, 3), padding='same')(img_input)
  x = BatchNormalization()(x)
  x_c_1 = Activation('relu')(x)
  x = Conv2D(conv_size, (3, 3), padding='same')(x_c_1)
  x = BatchNormalization() (x)
  x_c_2 = Activation('relu')(x)

  x_mp = []

  for i in range(nBlock):
    l = MaxPooling2D(2**(i+1))(x)
    l = Conv2D(conv_size, (3, 3), padding='same', activation='relu') (l)
    l = Conv2DTranspose(conv_size, (2**(i+1), 2**(i+1)), strides=(2**(i+1), 2**(i+1)), activation='relu')(l)
    x_mp.append(l)
  
  fin = concatenate([img_input, x_c_1, x_c_2] + x_mp)
  fin = Conv2D(conv_size, (3, 3), padding='same')(fin)
  fin = BatchNormalization()(fin)
  fin = Activation('relu')(fin)
  fin = Conv2D(conv_size, (3, 3), padding='same')(fin)
  fin = BatchNormalization()(fin)
  fin = Activation('relu')(fin)

  fin = Conv2D(n_classes, (3, 3), activation='softmax', padding='same')(fin)

  мод = Model(img_input, fin)
  print('Создана модель нейронной сети!')
  мод.compile(loss='categorical_crossentropy', optimizer=Adam(lr=3e-4), metrics =[точность])
  return мод


def обучение_модели(модель, x_train, y_train, x_test, y_test, batch_size=None, epochs=None, коэф_разделения = 0.2):
  if batch_size == None:
    batch_size = int(x_train.shape[0] * 0.01)
  if epochs == None:
    epochs = 10
  filepath="model.h5"
  model_checkpoint_callback = ModelCheckpoint(
    filepath=filepath,
    save_weights_only=True,
    monitor='val_loss',
    mode='min',
    save_best_only=True)
  history = модель.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_data = (x_test, y_test), callbacks=[model_checkpoint_callback])
  модель.load_weights('model.h5')
  plt.figure(figsize=(12, 6)) # Создаем полотно для визуализации
  keys = list(history.history.keys())
  plt.plot(history.history[keys[0]], label ='Обучающая выборка') # Визуализируем график ошибки на обучающей выборке
  plt.plot(history.history['val_'+keys[0]], label ='Проверочная выборка') # Визуализируем график ошибки на проверочной выборке
  plt.legend() # Выводим подписи на графике
  plt.title('График ошибки обучения') # Выводим название графика
  plt.show()
  plt.figure(figsize=(12,6)) # Создаем полотно для визуализации
  plt.plot(history.history[keys[1]], label ='Обучающая выборка') # Визуализируем график точности на обучающей выборке
  plt.plot(history.history['val_'+keys[1]], label ='Проверочная выборка') # Визуализируем график точности на проверочной выборке
  plt.legend() # Выводим подписи на графике
  plt.title('График точности обучения') # Выводим название графика
  plt.show()

def тест_модели(модель, тестовый_набор, правильные_ответы, классы):
  number = np.random.randint(тестовый_набор.shape[0]) # Задаем индекс изображения в тестовом наборе
  sample = тестовый_набор[number]
  if sample.shape == (784,):
    sample = sample.reshape((28,28))  
  if sample.shape == (28, 28, 1):
    sample = sample.reshape((28,28))
  print('Тестовое изображение:')
  plt.imshow(sample, cmap='gray') # Выводим изображение из тестового набора с заданным индексом
  plt.axis('off') # Отключаем оси
  plt.show() 

  cars = классы
  sample = тестовый_набор[number].reshape((1 + модель.input.shape[1:]))
  pred = модель.predict(sample)[0] # Распознаем изображение с помощью обученной модели
  print()
  print('Результат предсказания модели:')
  for i in range(len(классы)):
    print('Модель распознала модель ',cars[i],' на ',round(100*pred[i],2),'%',sep='')
  print()
  print()
  print('Правильные ответ: ', cars[правильные_ответы[number]])

def тест_модели_сегментации(**kwargs):
  сегментация.тест_модели(**kwargs)

def показать_график_обучения(**kwargs):
  keys = list(kwargs['статистика'].history.keys())
  for i in range(len(keys)//2):
    plt.figure(figsize=(12, 6)) # Создаем полотно для визуализации
    plt.plot(kwargs['статистика'].history[keys[i]], label ='Обучающая выборка') # Визуализируем график ошибки на обучающей выборке
    plt.plot(kwargs['статистика'].history['val_'+keys[i]], label ='Проверочная выборка') # Визуализируем график ошибки на проверочной выборке
    plt.legend() # Выводим подписи на графике
    if 'loss' in keys[i]:
      plt.title('График ошибки обучения модели') # Выводим название графика
    else:
      plt.title('График точности обучения модели') # Выводим название графика
    plt.show()

def загрузить_предобученную_модель():
  url = 'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1QYLIUQWWyqLvn8TCEAZiY7q8umv7lyYw' # Указываем URL-файла
  output = 'model.h5' # Указываем имя файла, в который сохраняем файл
  gdown.download(url, output, quiet=True) 
  model = load_model('model.h5')
  return model