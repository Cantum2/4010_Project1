// This makes me appreciate js frameworks a whole lot more..........
const tabCount = 4;
const cheesyHackerQuotes = ['Accessing the main frame', 'zoom/enhance', 'It\'s a UNIX system!',
 'Overriding security...', 'Turning it off then back on again...', 'This is the FBI open up!',
'Did you try deleting System 32?', 'ALT+F4 makes the page load faster'];

 const loadString = 'Just kidding your analysis will be up in 1 second';
 let quoteChangeCount = 0;

 /**
  * Handles the changing of the text under the loading gif
  * 
  */
 const interval = setInterval(() => {
     const randNum = Math.floor(Math.random() * Math.floor(cheesyHackerQuotes.length)); // max num between 0 and len of quotes arr
     document.getElementsByName('hacker-text')[0].innerHTML = quoteChangeCount < 4 ? cheesyHackerQuotes[randNum] : loadString;
     quoteChangeCount++;
 }, 1000);

 /**
  * After 6 seconds it hides the @var loadingdiv and shows the @var loadeddiv which are located in the html
  */
setTimeout(() => {
    document.getElementsByName('loaded-div')[0].style.display = 'block';
    document.getElementsByName('loading-div')[0].style.display = 'none';
    clearInterval(interval); 
}, 6000);

/**
 * Hides the current div, shows the selected div and applies the selected css class to the selected button while
 * also removing selected from previously selected
 * @param index - index of the tab selcted 
 */
function tabChanged(index) {
    for(let i =0; i < tabCount -1; i++){
        const divContent =  document.getElementsByName(i.toString())[0];
        const tabButton = document.getElementsByName(`tab-button-${i}`)[0];
        if(i === index) {
            divContent.style.display = 'block';
            tabButton.classList.remove('tab-button');
            tabButton.classList.add('tab-button-selected');
        }else {
            divContent.style.display = 'none';
            tabButton.classList.add('tab-button');
            tabButton.classList.remove('tab-button-selected');
        }
    }
}

/**
 * uoʇ ᴉɯdoɹʇɐuʇ
 */
function dontPressClicked(){
    document.getElementsByName('loaded-div')[0].style.display = 'none';
    document.getElementsByName('tabHolder')[0].style.display = 'none';
    document.body.classList.add('code-rain');
}