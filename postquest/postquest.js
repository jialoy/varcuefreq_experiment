String.prototype.format = function() {
    // string formatting
    var formatted = this;
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{'+i+'\\}', 'gi');
        formatted = formatted.replace(regexp, arguments[i]);
    }
    return formatted;
};

function random_remove_and_modify(array) {
    // selects and removes random element from array
    // returns selected element
	var randElement = array[Math.floor(Math.random()*array.length)];
    var index = array.indexOf(randElement);
    if (index != -1) {
        array.splice(index, 1);
    }
    return randElement;
}

function getDateTime(){
    // for the way Carmen is logging dates in main exp script
    var theDate = new Date();
    var days = ['Sun', 'Mon' , 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    theDate = days[theDate.getDay()] + ' ' + months[theDate.getMonth()] + ' ' + ' ' + theDate.getDate() + ' ' + ('0' + theDate.getHours()).slice(-2) + ":" + ('0' + theDate.getMinutes()).slice(-2) + ":" + ('0' + theDate.getSeconds()).slice(-2) + ' ' + theDate.getFullYear();

    return theDate;
}

//----------------------------------------------------------------
//-------functions to display/update stuff on each trial--------//

function display_text(text, size, parentId) {
    // append text in div to parent container
    var div = document.createElement("div");
    div.id = "textDiv";
    div.style.position = "absolute";
    div.style.top = (h/2-200).toString()+'px';
    div.style.left = (w/2-300).toString()+'px';
    div.style.width = '600px';
	div.style.backgroundColor = "#ffffff";
    div.style.textAlign = 'center';
    div.style.fontFamily = 'Arial';
    div.style.fontSize = size;
    div.innerHTML = text;

    document.getElementById(parentId).appendChild(div);
    
}

function remove_obj(parentId, childId) {
    // remov child object from parent container
    var child = document.getElementById(childId);
    document.getElementById(parentId).removeChild(child);
}

function display_textarea(parentId) {
    // create and append textarea object to parent container
    var textarea = document.createElement("textarea");
    textarea.id = "theTextfield";
    textarea.style.position = "absolute";
    textarea.style.top = (h/2-30).toString()+"px";
    textarea.style.left = (w/2-260).toString()+"px";
    textarea.style.width = '520px';
    textarea.style.height = '150px';
    div.appendChild(textarea);
    
    document.getElementById(parentId).appendChild(textarea);
    
}

function display_slider(parentId) {
	// create and append slider object to parent container
    var slider = document.createElement("input");
    slider.id = "theSlider";
    slider.setAttribute("type", "range");
    slider.setAttribute("min", "0");
	slider.setAttribute("max", "100");
    slider.style.width = "500px";
    slider.style.height = "25px";
    slider.style.position = "absolute";
    slider.style.top = (h/2).toString()+"px";
	slider.style.left = (w/2-250).toString()+"px";
	
    document.getElementById(parentId).appendChild(slider);
}

function reset_slider() {
	// resets slider value to middle
	document.getElementById("theSlider").value = "50";	
}

function display_range(parentId) {
	// create table with range values and append to parent container
	var theRange = [0, '', '', '', 100];
	var theText = ["Never", '', '', '', 'All the time'];
	
	var table = document.createElement("table");
    table.id = "rangeTable";
	table.style.position = "absolute";
	table.style.top = (h/2+50).toString()+"px";
	table.style.left = '0px';//(w/2-285).toString()+"px";
	table.style.width = (500/5*6).toString()+"px"; 	// make table width of slider plus one additional cell (for half cell padding at either end)
	document.getElementById(parentId).appendChild(table);
	
	var row = document.createElement("tr");
	row.style.borderSpacing = "100px";
	table.appendChild(row);
	
	for (var i=0; i<5; i++) {
		var cell = document.createElement("td");
        cell.id = "rangeCell";
		cell.style.position = "absolute";
		cell.style.width = "100px"; 	// make cell width 1/7 width of slider
		cell.style.left = ((590/5)*i).toString()+"px";
        cell.style.fontFamily = 'Arial';
		cell.style.textAlign = "center";
		cell.appendChild(document.createTextNode(theRange[i]));
		cell.appendChild(document.createElement("br"));
		cell.appendChild(document.createElement("br"));
		cell.appendChild(document.createTextNode(theText[i]));
		row.appendChild(cell);
	}
}

function display_button(parentId) {
    // create next button and append to screen
    var button = document.createElement("button");
    button.id = "button";
    button.innerHTML = "Next";
    button.style.position = "absolute";
    button.style.top = (h/2+200).toString()+'px';
    button.style.left = (w/2-50).toString()+'px';
    button.style.width = "100px";
    button.style.height = "30px";
    
    document.getElementById(parentId).appendChild(button);
	return(button);
}

function get_previous_response(objID) {
    // get response (text input or slider) from previous question 
    var response = document.getElementById(objID).value;
    return response;
}

function send_trial_data(dataToSend) {
    // create form object, append data to form, send data via sendTrialData.php script
    var data = new FormData();
    data.append("data" , dataToSend);
    var xhr = new XMLHttpRequest(),
        method = 'POST',
        url = 'sendTrialData.php';
    xhr.open(method, url, true);
    xhr.send(data);
}

function initialise_first_trial(parentId) {
	// presents first question
	var i = 0;

	display_text(questions[i], "30px", parentId);
    display_textarea("mainDiv");
}


//-------------------------------------------------------------
//---------divs, vars and lists that we will need------------//

var speakerGroups = ['male speakers', 'female speakers'];

// stuff for logging
var params = new URLSearchParams(document.location.search);
var pptID = params.get("id");
var condition = params.get("cond");
var cueDist = params.get("cd");
var varDist = params.get("vd");
var varType = params.get("vt");
var majCat = params.get("mg");
var majMarker = params.get("mj");
var minMarker = params.get("mn");
var markers = [majMarker, minMarker];

//var majorityMarker, minorityMarker;
//if (majVar != 'NA') {
//    if (majVar=='fim') {
//        majorityMarker = 'fim';
//        minorityMarker = 'hap';
//    } else if (majVar == 'hap') {
//        majorityMarker = 'hap';
//        minorityMarker = 'fim';
//    }
//} else {
//    majorityMarker = random_remove_and_modify(markers);
//    minorityMarker = random_remove_and_modify(markers);
//}

var majoritySpeakers;
if (majCat != 'NA') {
    if (majCat == 'm') {
        majoritySpeakers = 'male speakers';
    } else if (majCat == 'f') {
        majoritySpeakers = 'female speakers';
    }  
} else {
    majoritySpeakers = random_remove_and_modify(speakerGroups);
}


var currBlock = 'Questionnaire';

// questions and things
var questions = ["What do {0} and {1} describe in Panitok?".format(majMarker, minMarker),
                 "In the final spoken test, when did you use {0} and when did you use {1}? Why?".format(majMarker, minMarker),
                 "Do you think the speakers of Panitok you met belonged to distinct groups? If so, how would you describe these groups?",
                 "You met speakers of Panitok from two groups - male and female. Were there the same number of speakers in each group? If not, which group had more speakers?",
                 "Would you say these groups of speakers used {0} and {1} differently? In what way?".format(majMarker, minMarker),
                 "When you were learning Panitok from the 8 speakers, what percentage of the time did {0} occur?".format(majMarker),
                 "What percentage of the time did {0} occur?".format(minMarker),
                 "When you were learning Panitok from the 8 speakers, what percentage of the time did {0} use '{1}'?".format(majoritySpeakers, majMarker),
                 "What percentage of the time did {0} use '{1}'?".format(majoritySpeakers, minMarker),
                 "Which languages do you speak?"];

var endText = 'That is all the Panitok you will learn today.\n\nThank you very much for your interest in my language.\n\nTenkyu, na gude!';


// this is the main div
var div = document.createElement("div");
div.id = 'mainDiv';
div.style.position = 'absolute';
div.style.top = '0px';
div.style.left = '0px';
div.style.height = '100%';
div.style.width = '100%';
document.body.appendChild(div);

// get div width and height
var w = document.getElementById('mainDiv').clientWidth;
var h = document.getElementById('mainDiv').clientHeight;

// div for range value on slider response trials
var div = document.createElement("div");
div.id = 'valueDiv';
div.style.position = 'absolute';
div.style.top = (h/2+100).toString()+"px";
div.style.left = (w/2-50).toString()+"px";
div.style.height = "50px";
div.style.width = "100px";
div.style.fontFamily = "Arial";
div.style.fontSize = "30px";
div.style.textAlign = "center";
document.getElementById("mainDiv").appendChild(div);

// div for table to display range valueson slider response trials
var div = document.createElement("div");
div.id = 'tableDiv';
div.style.position = 'absolute';
div.style.top = '0px';
div.style.left = (w/2-300).toString()+'px';
div.style.height = '100%';
div.style.width = '600px';
document.getElementById("mainDiv").appendChild(div);


//---------------------------------------------------------------------
//------event handler used to handle button click on each trial------//

var eventHandler = (function(){
    var i = 1; 	//initialise i as 1 since initialise_first_trial() calls sentences[0]
	var button = display_button("mainDiv");
	return function() {
        remove_obj("mainDiv", "textDiv");
        display_text(questions[i], "30px", "mainDiv");
        var dateTime = getDateTime();
        var response;
        var globalTrialNo = String(questions[i-1]).replace(/,/g, '');
        var trialNo = i;
        if (i >= 1 && i < 5) {
            response = get_previous_response("theTextfield").replace(/,/g, ' ');
            remove_obj("mainDiv", "theTextfield");
            display_textarea("mainDiv");
        } else if (i == 5) {
            response = get_previous_response("theTextfield").replace(/,/g, ' ');
            remove_obj("mainDiv", "theTextfield");
            display_range("tableDiv");
            display_slider("mainDiv");
            valueDiv.innerHTML = theSlider.value;
            theSlider.onchange = function() {
                valueDiv.innerHTML = theSlider.value;
            };
        } else if (i >= 6 && i < 9) {
            response = get_previous_response("theSlider");
            remove_obj("mainDiv", "theSlider");
            display_range("tableDiv");
            display_slider("mainDiv");
            valueDiv.innerHTML = '50';
            theSlider.onchange = function() {
                valueDiv.innerHTML = theSlider.value;
            };
        } else if (i >= 9 && i < 10) {
            response = get_previous_response("theSlider");
            remove_obj("mainDiv", "theSlider");
            tableDiv.innerHTML = '';
            valueDiv.innerHTML = '';
            display_textarea("mainDiv");
        } else if (i == 10) {
            response = get_previous_response("theTextfield").replace(/,/g, ' ');
            mainDiv.innerHTML = '';
            document.getElementById('mainDiv').style.whiteSpace = 'pre';
            display_text(endText, "30px", "mainDiv");
		}
        console.log(i);
        console.log(response);
        var dataToLog = [pptID, 'B', condition, cueDist, varDist, varType, markers, majCat, majMarker, currBlock, 'NA', 'NA', globalTrialNo, trialNo, 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA','NA', 'NA', '', response, dateTime, '\n'];
        send_trial_data(pptID + "+" + dataToLog);
        i++; 	// increment i *after* logging previous trial response 
	};
}());

//----------------------------------------------------
//---------------experiment begins------------------//

console.log(getDateTime());
console.log([pptID, condition, cueDist, varDist, varType]);

// send header to data file
send_trial_data(pptID + "+" + ['ID', 'study', 'condition', 'cueDist', 'varDist', 'varType', 'markers', 'majCat', 'majVar', 'phase', 'selectionTask', 'trialType', 'globalTrial', 'localTrial', 'nounItem', 'number', 'inputMarker', 'inputNoun', 'targetPosition', 'clickPosition', 'foilItem', 'foilNumber', 'category', 'foilCategory', 'speaker', 'targetSpeaker', 'foilSpeaker', 'spokenResponse', 'answerQuest', 'timeStamp', '\n']);

// present first trial on screen, then initialise event handler associated with button
// to respond to button click at the end of each trial

initialise_first_trial("mainDiv");
button.onclick = eventHandler;
