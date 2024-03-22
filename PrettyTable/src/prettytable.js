/*
 * Copyright (c) 2017 Berk SOYSAL
 * PrettyTable v1.0 - 06.03.2017
 */

function PrettyTable(options){
	this._options = null;
	this._init(options);
  this._table;
}

PrettyTable.prototype._init = function (options) {
	this._options = options;
	
  if(!options.container || !options.row || !options.column || !options.header){
    console.log('Error: PrettyTable --> missing field.');
    return;
  }
  if(options.header.length !== options.column){
    console.log('Error: PrettyTable --> header.len() != column.len()');
    return;
  }
  this.createTable();
}


PrettyTable.prototype.addRow = function (rowdata){
  var cols = this._options.column;
  var row = document.createElement('div');
  row.setAttribute('class','row');
  for(var j=0;j<cols;j++){
    var cell = document.createElement('span');
    cell.setAttribute('class','cell');
    
    if(this._options.hover) cell.setAttribute('title',rowdata[j])
    cell.innerHTML = rowdata[j];
    row.appendChild(cell);
  }
  if(this._table) this._table.appendChild(row);
}


PrettyTable.prototype.removeRow = function (rowNumber){
  if(rowNumber === 0){
    console.log('Error: PrettyTable --> Cannot remove the header');
    return;
  }
  if(!rowNumber){
    console.log('Error: PrettyTable --> No rows selected');
    return;
  }
  if(isNaN(rowNumber)){
    console.log('Error: PrettyTable --> Not a number');
    return;
  }
  if(rowNumber > this._table.childNodes.length || rowNumber < 0){
    console.log('Error: PrettyTable --> Row does not exist');
    return;
  }
  
  if(this._table) 
    this._table.removeChild(this._table.childNodes[rowNumber]); 
}


PrettyTable.prototype.createTable = function(){
	this._table = document.createElement('div');
	this._table.setAttribute('class','pretty-table');
  
  if(this._options.margin) var margin = 'margin:' + this._options.margin +';';
  else var margin = "";

  if(this._options.color) var color = 'color:' + this._options.color +';';
  else var color = "";

  if(this._options.fontWeight) var fontWeight = 'font-weight:' + this._options.fontWeight +';';
  else var fontWeight = "";

  if(this._options.align) var align = 'text-align:' + this._options.align +';';
  else var align = "";

  this._table.setAttribute('style',margin + color + fontWeight + align);

	var header = document.createElement('div');
	header.setAttribute('class','header');

  if(this._options.headerTextColor) var headerTextColor = 'color:'+ this._options.headerTextColor +';';
  else var headerTextColor = "";

  if(this._options.headerColor) var headerColor = 'background:' + this._options.headerColor +';';
  else var headerColor = "";
  header.setAttribute('style', headerTextColor + headerColor);

  var rows = this._options.row;
  var cols = this._options.column;

	for(var i=0;i<cols;i++){
		var cell = document.createElement('span');
		cell.setAttribute('class','cell');
		cell.innerHTML = this._options.header[i];
		header.appendChild(cell);
	}

	this._table.appendChild(header);

	if(this._options.data){
    for(var i=0;i<rows;i++){
  		var row = document.createElement('div');
  		row.setAttribute('class','row');
  		var rowdata = this._options.data.slice(i*cols,(i+1)*cols);
      
      this.addRow(rowdata);
  	}
  }

	this._options.container.appendChild(this._table);
}
