// Uses a cat gif api to generate a random cat gif for every submission.

window.onload = function() {
    fetch('https://cataas.com/cat/gif')
        .then(response => response.blob())
        .then(gifBlob => {
            const gifUrl = URL.createObjectURL(gifBlob);
            const imgElement = document.createElement('img');
            imgElement.src = gifUrl;
            document.getElementById('catGif').appendChild(imgElement);
        })
        .catch(error => {
            console.error('Error fetching cat GIF:', error);
        });
    };