import subprocess
from subprocess import STDOUT, check_call
import os, time
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.preprocessing import image
from IPython import display
from tensorflow.keras.utils import to_categorical, plot_model # Полкючаем методы .to_categorical() и .plot_model()
from tensorflow.keras import datasets # Подключаем набор датасетов
import importlib.util, sys, gdown
from . import сегментация

def распаковать_архив(откуда='', куда=''):
  proc = subprocess.Popen('unzip -q "' + откуда + '" -d ' + куда, shell=True, stdin=None, stdout=open(os.devnull,"wb"), stderr=STDOUT, executable="/bin/bash")
  proc.wait()

def показать_примеры(**kwargs):
  if 'путь' in kwargs:
    count = len(os.listdir(kwargs['путь']))
    fig, axs = plt.subplots(1, count, figsize=(25, 5)) #Создаем полотно из 3 графиков
    for i in range(count): #Проходим по всем классам
      car_path = kwargs['путь'] + '/' + os.listdir(kwargs['путь'])[i] + '/'#Формируем путь к выборке
      img_path = car_path + np.random.choice(os.listdir(car_path)) #Выбираем случайное фото для отображения
      axs[i].imshow(image.load_img(img_path, target_size=(108, 192))) #Отображение фотографии
      axs[i].axis('off') # отключаем оси
    plt.show() #Показываем изображения
  elif ('изображения' in kwargs):
    if 'метки' in kwargs:
      count = kwargs['метки'].max() # Задачем количество примеров
    elif 'количество' in kwargs:
      count = kwargs['количество'] # Задачем количество примеров
    else:
      count = 5
    f, axs = plt.subplots(1,count,figsize=(22,5)) # Создаем полотно для визуализации
    idx = np.random.choice(kwargs['изображения'].shape[0], count) # Получаем 5 случайных значений из диапазона от 0 до 60000 (x_train_org.shape[0])
    for i in range(count):
      axs[i].imshow(kwargs['изображения'][idx[i]], cmap='gray') # Выводим изображение из обучающей выборки в черно-белых тонах
      axs[i].axis('off')
    plt.show()
    if 'метки' in kwargs:
      print('Правильные ответы:',kwargs['метки'][(idx)]) # Выводим соответствующие правильные ответы из y_train_org

def показать_примеры_сегментации(**kwargs):
  сегментация.show_sample(**kwargs)

def создать_выборки(путь, размер, коэф_разделения=0.9):
  x_train = [] # Создаем пустой список, в который будем собирать примеры изображений обучающей выборки
  y_train = [] # Создаем пустой список, в который будем собирать правильные ответы (метки классов: 0 - Феррари, 1 - Мерседес, 2 - Рено)
  x_test = [] # Создаем пустой список, в который будем собирать примеры изображений тестовой выборки
  y_test = [] # Создаем пустой список, в который будем собирать правильные ответы (метки классов: 0 - Феррари, 1 - Мерседес, 2 - Рено)
  for j, d in enumerate(os.listdir(путь)):
    files = sorted(os.listdir(путь + '/'+d))    
    count = len(files) * коэф_разделения
    for i in range(len(files)):
      sample = image.load_img(путь + '/' +d +'/'+files[i], target_size=(размер[0], размер[1])) # Загружаем картинку
      img_numpy = np.array(sample) # Преобразуем зображение в numpy-массив
      if i<count:
        x_train.append(img_numpy) # Добавляем в список x_train сформированные данные
        y_train.append(j) # Добавлеям в список y_train значение 0-го класса
      else:
        x_test.append(img_numpy) # Добавляем в список x_test сформированные данные
        y_test.append(j) # Добавлеям в список y_test значение 0-го класса
  print('Созданы выборки: ')
  x_train = np.array(x_train) # Преобразуем к numpy-массиву
  y_train = np.array(y_train) # Преобразуем к numpy-массиву
  x_test = np.array(x_test) # Преобразуем к numpy-массиву
  y_test = np.array(y_test) # Преобразуем к numpy-массиву
  x_train = x_train/255.
  x_test = x_test/255.
  print('Размер сформированного массива x_train:', x_train.shape)
  print('Размер сформированного массива y_train:', y_train.shape)
  print('Размер сформированного массива x_train:', x_test.shape)
  print('Размер сформированного массива y_train:', y_test.shape)
  return (x_train, y_train), (x_test, y_test)

def предобработка_данных(**kwargs):
  if kwargs['сетка'] == 'полносвязная':
    x_train = kwargs['изображения']/255. # Нормируем изображения, приводя каждое значение пикселя к диапазону 0..1
    x_train = x_train.reshape((-1, 28*28)) # Изменяем размер изображения, разворачивая в один вектор
    print('Размер сформированных данных:', x_train[0].shape) # Выводим размер исходного изображения
    return x_train
  elif kwargs['сетка'] == 'сверточная':
    x_train = kwargs['изображения']/255. # Нормируем изображения, приводя каждое значение пикселя к диапазону 0..1
    x_train = x_train.reshape((-1, 28,28,1)) # Изменяем размер изображения, разворачивая в один вектор
    print('Размер сформированных данных:', x_train[0].shape) # Выводим размер исходного изображения
    return x_train

def загрузить_базу_АВТОМОБИЛИ():
  if 'путь' in kwargs:
	  path = '/content/drive/MyDrive/' + kwargs['путь'] + 'AIU.zip'
  else:
	  path = '/content/drive/MyDrive/AIU.zip'
  print('Загрузка данных')
  print('Это может занять несколько минут...')
  распаковать_архив(
    откуда = path,
    куда = '/content'
  )
  распаковать_архив(
      откуда = "middle_fmr3.zip",
      куда = "/content/cars"
  )
  display.clear_output(wait=True)
  print('Загрузка данных (Готово)')
  print('База загружена в Google Colaboratory')
  return
  
  urls = ['https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1sC5RGar5Oc4cqz3uk68-EGldThNykWMR',
            'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1RC-jMLoV9-E_cs2bh76sy77GLzPig0Xj',
            'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1XsO_SmDhiz-tfbYp2Ec7q-y8inakC7SG',
            'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1qcWpVl5Xk_QqdbM7OBNrMcrOMJjz9N0X',
            'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1fEPJMSNb2lhgi6djd75pZKAooXu5M6NQ']
  for url in urls:    
    output = 'middle_fmr.zip' # Указываем имя файла, в который сохраняем файл
    gdown.download(url, output, quiet=True) # Скачиваем файл по указанному URL
    display.clear_output(wait=True)
    if os.path.exists('middle_fmr.zip'):
        break
  
  # Скачиваем и распаковываем архив
  распаковать_архив(
      откуда = "middle_fmr.zip",
      куда = "/content/cars"
  )
  display.clear_output(wait=True)
  print('Загрузка данных (Готово)')
  print('База загружена в Google Colaboratory')

def загрузить_базу_МНИСТ():
  (x_train_org, y_train_org), (x_test_org, y_test_org) = datasets.mnist.load_data() # Загружаем данные набора MNIST
  display.clear_output(wait=True)
  print('Данные загружены')
  print('Размер обучающей выборки:', x_train_org.shape) # Отобразим размер обучающей выборки
  print('Размер тестовой выборки:', x_test_org.shape) # Отобразим размер тестовой выборки
  return (x_train_org, y_train_org), (x_test_org, y_test_org)

def загрузить_базу_ОДЕЖДА():
  (x_train_org, y_train_org), (x_test_org, y_test_org) = datasets.fashion_mnist.load_data() # Загружаем данные набора MNIST
  display.clear_output(wait=True)
  print('Данные загружены')
  print('Размер обучающей выборки:', x_train_org.shape) # Отобразим размер обучающей выборки
  print('Размер тестовой выборки:', x_test_org.shape) # Отобразим размер тестовой выборки
  return (x_train_org, y_train_org), (x_test_org, y_test_org)

def загрузить_базу_САМОЛЕТЫ():
  if 'путь' in kwargs:
	  path = '/content/drive/MyDrive/' + kwargs['путь'] + 'AIU.zip'
  else:
	  path = '/content/drive/MyDrive/AIU.zip'
  print('Загрузка данных')
  print('Это может занять несколько минут...')
  распаковать_архив(
    откуда = path,
    куда = '/content'
  )
  распаковать_архив(
      откуда = "Самолеты.zip",
      куда = "/content"
  )
  распаковать_архив(
      откуда = "Сегменты.zip",
      куда = "/content"
  )
  display.clear_output(wait=True)
  print('Загрузка данных (Готово)')
  print('База загружена в Google Colaboratory')
  return
  
  
  print('Загрузка данных...')
  url = 'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1_UL89O_OleR2ds35WVMLjTPUf34AchJ2' # Указываем URL-файла
  output = 'самолеты.zip' # Указываем имя файла, в который сохраняем файл
  gdown.download(url, output, quiet=True) # Скачиваем файл по указанному URL
  # Скачиваем и распаковываем архив
  распаковать_архив(
      откуда = "самолеты.zip",
      куда = "/content"
  )
  url = 'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=10ljOQIolCiCOvPo5bqWpaDTHDRIazNE4' # Указываем URL-файла
  output = 'сегменты.zip' # Указываем имя файла, в который сохраняем файл
  gdown.download(url, output, quiet=True) # Скачиваем файл по указанному URL
  # Скачиваем и распаковываем архив
  распаковать_архив(
      откуда = "сегменты.zip",
      куда = "/content"
  )
  display.clear_output(wait=True)
  print('Загрузка данных (Готово)')
  print('База загружена в Google Colaboratory')

def загрузить_базу_БОЛЕЗНИ():
  if 'путь' in kwargs:
	  path = '/content/drive/MyDrive/' + kwargs['путь'] + 'AIU.zip'
  else:
	  path = '/content/drive/MyDrive/AIU.zip'
  print('Загрузка данных')
  print('Это может занять несколько минут...')
  распаковать_архив(
    откуда = path,
    куда = '/content'
  )
  # Скачиваем и распаковываем архив
  распаковать_архив(
      откуда = "origin.zip",
      куда = "/content/diseases"
  )
  распаковать_архив(
      откуда = "segmentation.zip",
      куда = "/content/diseases"
  )
  display.clear_output(wait=True)
  print('Загрузка данных (Готово)')
  print('База загружена в Google Colaboratory')
  return
  
  print('Загрузка данных...')
  urls = ['https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1lI6tzfcdo1AAp-BejX8CvO9-8z9hZSX8',
            'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1v11AjlToMvtKWIi3QLM_i3JQRBBoZt7d',
            'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1x0f96bddPBnZ6B0l3bky21Hj0xPDpHWW'
            'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1nbX_FrjnDxyiLIEqX11wMZ8JWqNkPrav',
            'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1OHz3XerVtjeq1o0xXjbTs_FM7cve3ftP',
            'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1ITxxBmAlQaKm80Fdte_8Qz1Df-b2t9JE',
            'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1JWQ1QQ6BEcV_aBHV-jK8bp1675Rq1Nva',
            'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=15MS4mtipyek-dpEiZE66uWIsX7NovDNv']
  for url in urls:    
    output = 'diseases.zip' # Указываем имя файла, в который сохраняем файл
    gdown.download(url, output, quiet=True) # Скачиваем файл по указанному URL
    display.clear_output(wait=True)
    if os.path.exists('diseases.zip'):
        break  
  # Скачиваем и распаковываем архив
  распаковать_архив(
      откуда = "diseases.zip",
      куда = "/content/diseases"
  )
  urls = ['https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1IKUFITFRfvoauc2KAkagb7Ep45bpmZRj',
          'https://drive.google.com/uc?export=download&amp;confirm=no_antivirus&amp;id=18QB4n2t4E4N6LhCwWzMknNrzoz3oNSTZ',
          'https://drive.google.com/uc?export=download&amp;confirm=no_antivirus&amp;id=17FHkRvZEog1I3anFnz9gOfOZAU8kBZC9',
          'https://drive.google.com/uc?export=download&amp;confirm=no_antivirus&amp;id=12lZTD6PUTReej62cQID7c0IDChukw2xK',
          'https://drive.google.com/uc?export=download&amp;confirm=no_antivirus&amp;id=1Gpc4Fy2W-2MhYs1bqLNdPAQJS-xvTfDU'
          ]
  for url in urls:    
    output = 'segm.zip' # Указываем имя файла, в который сохраняем файл
    gdown.download(url, output, quiet=True) # Скачиваем файл по указанному URL
    display.clear_output(wait=True)
    if os.path.exists('segm.zip'):
        break  
  # Скачиваем и распаковываем архив
  распаковать_архив(
      откуда = "segm.zip",
      куда = "/content/diseases"
  )
  display.clear_output(wait=True)
  print('Загрузка данных (Готово)')
  print('База загружена в Google Colaboratory')

def создать_выборки_для_сегментации(images_airplane, segments_airplane):
   return сегментация.create_xy(images_airplane, segments_airplane)

def обработка_изображений(**kwargs):
  return сегментация.get_images(**kwargs)
  
def загрузить_базу_СТРОЙКА(**kwargs):
  if 'путь' in kwargs:
	  path = '/content/drive/MyDrive/' + kwargs['путь'] + 'AIU.zip'
  else:
	  path = '/content/drive/MyDrive/AIU.zip'
  if 'быстрая_загрузка' not in kwargs:
	  print('Загрузка данных')
	  print('Это может занять несколько минут...')
	  распаковать_архив(
		откуда = '/content/drive/MyDrive/AIU.zip',
		куда = '/content'
	  )
	  распаковать_архив(
		  откуда = "Notebooks.zip",
		  куда = "/content"
	  )
	  x_train = np.load('xTrain_st.npy')
	  x_test = np.load('xVal_st.npy')
	  y_train = np.load('yTrain_st.npy')
	  y_test = np.load('yVal_st.npy')  
	  print('Загрузка данных (Готово)')
	  return (x_train, y_train), (x_test, y_test)
  else:
	  print('Загрузка данных...')
	  urls = ['https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1WtUbopKzQw97W8DChDu0JidJYh08XQyy',
				'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=14gsGpYv13IMUKXmjQEPhPt2bVpVkcJfY',
				'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1A9IThR5f7dUIHgohDDJBeFyAZquTiYIL',
				'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1PtMhqaPXYoJKuKjLy338rBgv-PsScYPh',
				'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1qRAPeOgCZ0g9nikKmop4uWGEe9cCSm4B',
				'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1MDJiPs1Lyh-ij5dldjAu-kwWWb2uPNKi',
				'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1S7bc5yR2fHsR81aDZsIpBcCfxf-43Cek'
				'']
	  for url in urls:    
		output = 'data.zip' # Указываем имя файла, в который сохраняем файл
		gdown.download(url, output, quiet=True) # Скачиваем файл по указанному URL
		if os.path.exists('data.zip'):
			break  
	  # Скачиваем и распаковываем архив
	  распаковать_архив(
		  откуда = "data.zip",
		  куда = "/content"
	  )
	  x_train = np.load('xTrain_st.npy')
	  x_test = np.load('xVal_st.npy')
	  y_train = np.load('yTrain_st.npy')
	  y_test = np.load('yVal_st.npy')  
	  print('Загрузка данных (Готово)')
	  return (x_train, y_train), (x_test, y_test)