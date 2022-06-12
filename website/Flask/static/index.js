/* index.js 
const log = console.log

var inputs, index, counter, value;
var playCards = [];

document.getElementById("button").addEventListener("click", 
    function()
    {
        inputs = document.getElementsByClassName('playInput');
        counter = 0;
        for (index = 0; index < inputs.length; ++index) {
            value = parseInt(inputs[index].value)
            if (!isNaN(value))
            {
                playCards[counter] = parseInt(inputs[index].value);
                counter++;
            }
            else
            {
                
            }
        }
        counter = 0;
        log(playCards);
    }
);*/