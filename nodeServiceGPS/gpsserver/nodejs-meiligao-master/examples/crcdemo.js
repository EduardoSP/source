var crc = require('crc');

var peticion  = "2424001220160302ffffff08000bd1df0d0a";
var respuesta = "4040001220160302ffffff08010b58a50d0a";



var binary = new Buffer("2424001120160302ffffff5000", 'hex').toString('binary');

//console.log("2424001220160302ffffff08000ac1fe0d0a".substring(26,28));
console.log(crc.crc16ccitt(binary).toString(16));

console.log(crc.crc16ccitt(new Buffer("2424001220160302ffffff08000b", 'hex')).toString(16));

console.log(crc.crc16ccitt(new Buffer("4040001220160302ffffff08010b", 'hex')).toString(16));


//4040001220160302ffffff08010cabc90d0a
console.log(crc.crc16ccitt(new Buffer("4040001220160302ffffff08010c", 'hex')).toString(16));

