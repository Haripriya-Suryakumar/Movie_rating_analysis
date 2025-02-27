document.addEventListener("DOMContentLoaded", function () {
    const genreElement = document.querySelector(".genre-hover");
    const genreChart = document.querySelector("#genreChart");
    const similarMoviesButton = document.querySelector("#showSimilar");
    const similarMoviesDiv = document.querySelector("#similarMovies");

    // Genre meter visualization
    if (genreElement) {
        genreElement.addEventListener("mouseover", function () {
            const genreData = JSON.parse(genreElement.getAttribute("data-genres")); 
            drawGenreChart(genreData);
        });
    }

    // Show similar movies button
    if (similarMoviesButton) {
        similarMoviesButton.addEventListener("click", function () {
            const movieTitle = document.querySelector("#movieTitle").innerText;
            fetch(`/similar_movies?title=${movieTitle}`)
                .then(response => response.json())
                .then(data => {
                    similarMoviesDiv.innerHTML = `<h3>Similar Movies:</h3><ul>` +
                        data.movies.map(movie => `<li>${movie}</li>`).join('') +
                        `</ul>`;
                });
        });
    }
});

// Function to draw genre meter visualization
function drawGenreChart(genreData) {
    genreChart.innerHTML = ""; 
    let total = Object.values(genreData).reduce((sum, value) => sum + value, 0);

    for (let genre in genreData) {
        let width = (genreData[genre] / total) * 100;
        let div = document.createElement("div");
        div.style.width = width + "%";
        div.style.height = "20px";
        div.style.background = getGenreColor(genre);
        div.style.display = "inline-block";
        div.title = `${genre}: ${genreData[genre]}%`;
        genreChart.appendChild(div);
    }
}

// Function to get color based on genre
function getGenreColor(genre) {
    const colors = {
        "Action": "#ff5733",
        "Adventure": "#f4c842",
        "Sci-Fi": "#33aaff",
        "Drama": "#ff33aa",
        "Comedy": "#33ff77",
    };
    return colors[genre] || "#ddd";
}
