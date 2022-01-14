# Carriage Return Bible Versifier

This piece of software takes an html bible (generated with [Haiola](https://haiola.org/)), and converts these to a JSON file of "verses by paragraph".

An example of the output is as follows:

```json
{
  "Genesis": {
    "01": [
      [1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [9, 10, 11, 12, 13],
      [14, 15, 16, 17, 18, 19],
      [20, 21, 22, 23],
      [24, 25],
      [26, 27, 28, 29, 30]
    ]
  }
}
```

This dataset was taken from the [World English Bible British Edition](https://ebible.org/find/details.php?id=engwebpb) (because these Bibles are in the public domain).

## Arguments

```
> python .\main.py -h
usage: main.py [-h] --folder FOLDER --xmlname XMLNAME

A software for getting verse positions by paragraph

optional arguments:
  -h, --help            show this help message and exit
  --folder FOLDER, -f FOLDER
                        choose the folder with the bible dataset
  --xmlname XMLNAME, -x XMLNAME
                        select the name of the xml file (don't pass a path)
```

For example, on the [World English Bible British Edition](https://ebible.org/find/details.php?id=engwebpb):

```
> python .\main.py -f .\engwebpb_html\ -x engwebpb-VernacularParms.xml
```

## Other Information

This software has _ONLY_ been tested on the "World English Bible British Edition" because that is the bible I was analysing this text!
