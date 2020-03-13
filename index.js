// This makes me appreciate js frameworks a whole lot more..........

const cheesyHackerQuotes = ['Accessing the main frame', 'zoom/enhance', 'It\'s a UNIX system!',
 'Overriding security...', 'Turning it off then back on again...', 'This is the FBI open up!',
'Did you try deleting System 32?', 'ALT+F4 makes the page load faster'];

 const loadString = 'Just kidding your analysis will be up in 1 second';
 let quoteChangeCount = 0;

 const interval = setInterval(() => {
     const randNum = Math.floor(Math.random() * Math.floor(cheesyHackerQuotes.length)); // max num between 0 and len of quotes arr
     document.getElementsByName('hacker-text')[0].innerHTML = quoteChangeCount < 4 ? cheesyHackerQuotes[randNum] : loadString;
     quoteChangeCount++;
 }, 1000);

setTimeout(() => {
    document.getElementsByName('loaded-div')[0].style.display = 'block';
    document.getElementsByName('loading-div')[0].style.display = 'none';
    clearInterval(interval); 
}, 6000);

function tabChanged(index) {
    console.log(index);
}