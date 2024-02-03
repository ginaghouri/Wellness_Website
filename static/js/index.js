document.addEventListener('DOMContentLoaded', (event) => {
    // fix the delay for retrieving timestamp
    (function(){
        // get date.
        const current = new Date();
    
        // update HTML with date object as a string.
        document.getElementById("timestamp").innerHTML = current.toLocaleString();
        setTimeout(arguments.callee, 1000);
    })();
    // self executing function.
});