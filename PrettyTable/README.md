<snippet>
<content>
# PrettyTable :bookmark:
PrettyTable is a tiny vanillaJS library that enables anyone to create pretty looking tables.

## Installation
Step 1 : Add the required css file to your HTML file inside the <head> tag:

```html
<head>
...
  <link rel="stylesheet" href="dist/prettytable-min.css">
</head>
```
Step 2 : Add the required javascript file to your HTML file at the end of the <body> tag:

```html
<body>
  ...
  <script type="text/javascript" src="dist/prettytable-min.js"></script>
</body>
```
## Usage
There are 4 required attributes to be able to create a new PrettyTable. These are 'container (DOM Object)','row (number)','column (number)' and 'header (array)'.

```js 

    var container = document.getElementById('tableContainer');
    var header = ["Column 1","Column 2","Column 3","Column 4","Column 5"];

    var options = {
      container: container,
      header:header,
      row:4,
      column:5
    };
    var table1 = new PrettyTable(options);
    // Adds a new row
    table1.addRow([0,1,2,3,"a"]);

```
![Example 1](https://4.bp.blogspot.com/-y8AfnzprG60/WJfyr77tGRI/AAAAAAAALQY/WEBRmW1HoOgsjrc5qHkxB7-YBrbWUbbjQCLcB/s1600/1.png)

Additionally PrettyTable supports many other attributes:

```js

    var options2 = {
      container: container,
      header:header,
      row:1,
      column:5,
      headerColor:'lightblue',
      headerTextColor:'black',
      fontWeight:'bold',
      margin:80,
      color:'red',
      align:'right',
      hover:true
    };
    var table2 = new PrettyTable(options2);
    table2.addRow([1,2,3,6,9]);
    table2.addRow([11,22,33,66,99]);
    table2.addRow([12,22,32,62,92]);
    table2.addRow([13,23,33,63,93]);
    table2.addRow([14,24,34,64,94]);
    // Removes the 4th row from this table
    table2.removeRow(4);
    
```
![Example 2](https://2.bp.blogspot.com/-HDZoWYQZ8o8/WJfysA-uIvI/AAAAAAAALQc/l38Ip--YCvU3bTNddjwtzezil8aui5nPACLcB/s1600/2.png)

It also supports adding data as an array. Here is a full example:

```js
   
    var data = ["a","b","c","d","e","f","<b>BOLD</b>","h","i","j","k","l",
    "<i>italic</i>","n","<u>underlined</u>","p","q","r"
    ,"<img src='http://1.bp.blogspot.com/-MxHUkmgRD_A/V-Fvzy42EII/AAAAAAAALAU/RsFOlb3cpk4l85NYlRQxyrEEqHoYH1ShgCK4B/s1600/Codemio.com.png' width='100' height='auto'></img>","t"];
    var options3 = {
      container: container,
      header:header,
      row:4,
      column:5,
      headerColor:'green',
      align:'center',
      data:data
    };
    var table3 = new PrettyTable(options3);
    table3.addRow(["<span style='color:blue'>BLUE</span>",12,13,16,92]);

```
![Example 3](https://3.bp.blogspot.com/-9yT7LuzdL6o/WJfyryD8kdI/AAAAAAAALQg/nmwf14-DljQMp74so9xUgMs_WtFMPH8_wCLcB/s1600/3.png)


## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :)

## Authors
* **Berk Soysal** - *Initial work* - [Herrberk](https://github.com/herrberk)

## Donate
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/codemio)
If you like this project and would like to contribute financially, please feel free to donate some coffee beans :) 


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
</content>
</snippet>
