/*
 * Copyright (c) 2017 Berk SOYSAL
 * PrettyTable v1.0 - 06.03.2017
 */


function testPrettyTable(){
  var container = document.getElementById('tableContainer');
  
  var data = ["a","b","c","d","e","f","<b>BOLD</b>","h","i","j","k","l",
  "<i>italic</i>","n","<u>underlined</u>","p","q","r"
  ,"<img src='http://1.bp.blogspot.com/-MxHUkmgRD_A/V-Fvzy42EII/AAAAAAAALAU/RsFOlb3cpk4l85NYlRQxyrEEqHoYH1ShgCK4B/s1600/Codemio.com.png' width='100' height='auto'></img>","t"];
  
  var header = ["Column 1","Column 2","Column 3","Column 4","Column 5"];
  
  /** First Table **/
  var options = {
    container: container,
    header:header,
    row:4,
    column:5
  };
  var table1 = new PrettyTable(options);
  // Adds a new row
  table1.addRow([0,1,2,3,"a"]);


  /** Second Table **/
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


  /** Third Table **/
  var options3 = {
    container: container,
    row:4,
    column:5,
    header:header,
    headerColor:'green',
    align:'center',
    data:data
  };
  var table3 = new PrettyTable(options3);
  table3.addRow(["<span style='color:blue'>BLUE</span>",12,13,16,92]);
}