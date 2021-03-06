# Step by Step algorithm of preprocessing

**Скачивание базы данных**
1) из `config/params.json` берем словарь `databases`. В нем содержатся названия базы данных и url, из которых можно скачать соответствующую базу данных
2) в папке `data` ищем базы данных с названиями из словаря `databases`. Если не находим - скачиваем. После этого у нас получается массив путей до баз данных с записями

**Распаковка сигналов**
1) Проходимся по всем базам данных и собираем все *сырые* записи сигналов в один большой массив
2) Проходимся по каждому сигналу из полученного массива
3) Так как сигнал ЭКГ может быть многоканальным, а мы хотим работать только с одним каналом, то разбиваем его на несколько и создаем соответствующее количество объектов классов `Signal`. По итогу получаем новый массив с одноканальными сигналами, готовыми к обработке

**Получение характеристик сигнала**
- **ЧАСТЬ I: получение окон**
    1) получаем индексы R-пиков ЭКГ сигнала
    2) делим всю запись ЭКГ сигнала на *окна* по `window_size` R-пиков в каждом. Значение `window_size` берем из `config/params.json`
    3) Сохраняем массив объектов класса `Window` в классе `Signal`
- **ЧАСТЬ II: обработка окон**
    1) построить последовательность отношений продолжительности R-R интервалов
    2) извлечь признаки из этой последовательности:
        - построить алфавит отношений на основе `treshold`
        - получить основные характеристики
- **ЧАСТЬ III: обучение**
    1) отметить здоровые и больные участки
    2) выделить выборки для тестов и тренировок
    3) запустить подбор гиперпараметров
