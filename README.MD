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

## How-to

1. Choose a copy of the bible from [ebible.org's download page](https://ebible.org/download.php). I personally chose [WEBPB](https://ebible.org/details.php?id=engwebpb).
2. Download the "Zipped mobile HTML" file. For WEBPB this was: `engwebpb_html.zip`.
3. Note down from this website the `ID` of your bible:
   ![ID](https://i.imgur.com/yrOvIf4.png)
4. Unzip this folder into a folder with the same name, i.e: `.\engwebpb_html`
5. Download a copy of CR_bible and extract it to your downloads folder. This created a folder called `CR_bible-master` for me.
6. Copy this folder to the same directory as CR_bible (the `CR_bible-master` folder)
7. Open a powershell in this folder (Shift+Right-Click `Open PowerShell window here`)
8. Execute the following command:

```
> python .\main.py -f .\<folder including bible>\ -x <bible ID>-VernacularParms.xml
```

For the WEBP:

```
> python .\main.py -f .\engwebpb_html\ -x engwebpb-VernacularParms.xml
```

9. Now you have this JSON, you can use this in your own projects, or you can move the `dataset.json` file into the same folder as [bible-maker](https://github.com/jimbob88/bible-maker) and execute the following command:

```
> python .\main.py -p .\dataset.json -o .\<bible>.txt
```
