var currentPlayer;
var player1Name;
var player2Name;
var gameName;

//tells if low or high
var player1Balls;
var player2Balls;

//list of balls on the table
var allBalls = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15];

$(document).ready(function () {

    // initalizePlayers();

    const svg = 'table-0.svg';
    const tableDiv = $('#svgInfo');

    // Variables
    let isMouseOverSVG = false;
    let isMouseDown = false;

    tableDiv.load(svg, () => {
        console.log('SVG loaded successfully');
        
        // Retrieve names and game state from local storage
        player1Name = localStorage.getItem('player1Name') || "Player 1";
        player2Name = localStorage.getItem('player2Name') || "Player 2";
        gameName = localStorage.getItem('gameName') || "New Game";
        currentPlayer = localStorage.getItem('currentPlayer');

        // Retrieve the array of all balls, parse it back into an array
        allBalls = JSON.parse(localStorage.getItem('allBalls')) || [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15];

        //inital display
        $('#gameNameDisplay').text(`Game Name: ${gameName}`);
        $('#player1Display').text(`Player 1: ${player1Name}`);
        $('#player2Display').text(`Player 2: ${player2Name}`);
        $('#turnDisplay').text("It's now " + currentPlayer + " turn");
        
        //show the diff balls low and high
        lowHighBallDisplay()

        // Once SVG is loaded, attach event listeners for mouse enter and leave
        const svgElement = $('#svgInfo svg');

        svgElement.mouseenter(function () {
            isMouseOverSVG = true;
        });

        svgElement.mouseleave(function () {
            isMouseOverSVG = false;
        });

        // Mouse down event on the SVG container
        $('#svgInfo').on('mousedown', function () {
            isMouseDown = true; // Set flag when mouse button is pressed
            showLine(event); // Show the line where the mouse is pressed
        });

        // Mouse up event on the entire document to handle button release anywhere
        $(document).on('mouseup', function () {
            if (isMouseDown && isMouseOverSVG) { // Ensure the mouse was down and over the SVG for a "shot"
                shotit(event);
            }
            isMouseDown = false; // Clear flag when mouse button is released
            hideLine(); // Hide the line
        });

        // Modify the existing mousemove on the div to check if the mouse is over the SVG
        $('#svgInfo').mousemove(function (event) {
            if (isMouseOverSVG && isMouseDown) {
                trackit(event);
            }
        });
    })

    // //start a new game button
    // document.getElementById('startNewGame').addEventListener('click', function () {
    //     window.location.href = 'shoot.html';
    // });
});

function showLine(event) {
    const svgElement = document.querySelector('#svgInfo svg');
    const line = svgElement.querySelector('#myLine');
    if (line) {
        line.setAttribute('visibility', 'visible');
    }
}

function hideLine() {
    const svgElement = document.querySelector('#svgInfo svg');
    const line = svgElement.querySelector('#myLine');
    if (line) {
        line.setAttribute('visibility', 'hidden');
    }
}

//send to server
function sendNames() {

    initalizePlayers()

    //send names to server
    const data = {
        player1: player1Name,
        player2: player2Name,
        game: gameName
    };

    //send names to server
    $.ajax({
        type: "POST",
        url: `http://localhost:52174/sendNames`,
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (result) {
           console.log(result);
           window.location.href = `http://localhost:52174/pool.html`;
        }
    })
}

function initalizePlayers() {
    console.log('Initializing players...');

    // Retrieve names from local storage
    player1Name = $("#player1Name").val()
    player2Name = $("#player2Name").val()
    gameName = $("#gameName").val()

    // Randomly decide who goes first
    currentPlayer = Math.random() < 0.5 ? player1Name : player2Name;

    //add to storage for when redirect to pool.html
    localStorage.setItem('player1Name', player1Name);
    localStorage.setItem('player2Name', player2Name);
    localStorage.setItem('gameName', gameName);
    localStorage.setItem('currentPlayer', currentPlayer);

    //allBalls is an array, we need to stringify it
    localStorage.setItem('allBalls', JSON.stringify(allBalls));

    //set low and high balls (randomized)
    // Randomly assign "High" and "Low" numbered balls to players
    // if (Math.random() < 0.5) {
    //     localStorage.setItem('player1Balls', 'Low (1-7)');
    //     localStorage.setItem('player2Balls', 'High (9-15)');
    // } else {
    //     localStorage.setItem('player1Balls', 'High (9-15)');
    //     localStorage.setItem('player2Balls', 'Low (1-7)');
    // }
}

function lowHighBallDisplay(){
    // $('#ballnumInfo').append();
    // $('#ballnumInfo').append();
}

function trackit(event) {
    const svgElement = document.querySelector('#svgInfo svg');
    if (!svgElement) {
        return;
    }

    const svgPoint = svgElement.createSVGPoint();
    svgPoint.x = event.clientX;
    svgPoint.y = event.clientY;

    // Convert the page coordinates to SVG coordinates
    const svgCoords = svgPoint.matrixTransform(svgElement.getScreenCTM().inverse());

    const cueBall = svgElement.querySelector('#ball0');
    if (!cueBall) {
        return;
    }
    // Extract cue ball position
    const cueBallX = cueBall.getAttribute("cx");
    const cueBallY = cueBall.getAttribute("cy");

    // Check for existing line, or create a new one
    let line = svgElement.querySelector('#myLine');
    if (!line) {
        line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("id", "myLine");
        line.setAttribute("stroke", "black");
        svgElement.appendChild(line);
    }

    // Update line attributes
    line.setAttribute("x1", cueBallX);
    line.setAttribute("y1", cueBallY);
    line.setAttribute("x2", svgCoords.x);
    line.setAttribute("y2", svgCoords.y);
}

function shotit(event) {

    // Define necessary constants
    const DRAG = 150.0; // mm/s^2
    const VEL_EPSILON = 0.01; // mm/s

    const svgElement = document.querySelector('#svgInfo svg');
    if (!svgElement) {
        return;
    }
    // Convert mouse release coordinates to SVG coordinates
    const svgPoint = svgElement.createSVGPoint();
    svgPoint.x = event.clientX;
    svgPoint.y = event.clientY;
    const releaseCoords = svgPoint.matrixTransform(svgElement.getScreenCTM().inverse());

    // Get cue ball
    const cueBall = svgElement.querySelector('#ball0');
    if (!cueBall) {
        return;
    }

    // Extract cue ball position
    const cueBallX = parseFloat(cueBall.getAttribute("cx"));
    const cueBallY = parseFloat(cueBall.getAttribute("cy"));

    // Compute initial velocity as the difference between release point and cue ball position
    const xvel = releaseCoords.x - cueBallX;
    const yvel = releaseCoords.y - cueBallY;

    console.log(`Initial velocity: vx=${xvel}, vy=${yvel}`);

    // Calculate the acceleration
    const speed = Math.sqrt(xvel * xvel + yvel * yvel);

    console.log(`speed=${speed} VEL_EPS=${VEL_EPSILON}`)

    // Initialize acceleration
    let accx = 0, accy = 0;

    if (speed > VEL_EPSILON) {
        let accx = ((xvel * -1.0) / speed) * DRAG;
        let accy = ((yvel * -1.0) / speed) * DRAG;
    }

    console.log(`Initial Acc: ax=${accx}, ay=${accy}`);

    // Hide the line
    hideLine();

    //animations - make cue ball move

    const data = {
        xvel: xvel,
        yvel: yvel,
        current: currentPlayer
    };

    //create post request and pass values
    $.ajax({
        type: "POST",
        url: "http://localhost:52174//process-shot",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (result) {
            // Handle successful response
            console.log("Shot processed:", result);

            const SVGDiv = $('#SVGInfo');

            //loop through and replace svg
            (function (index) {
                setTimeout(function () {
                    SVGDiv.empty();
                    SVGDiv.append(tableSVG[index]);
                }, i * 1000);
            })(i);

            //change turns
            changeTurns();
        },
        error: function (error) {
            console.error("Error processing shot:", error);
        }
    });
}

function svgElementFromString(str) {
    const div = document.getElementById('svgInfo');
    div.innerHTML = str;

    const svg = div.querySelector('svg');

    if (!svg) {
        throw Error('<svg> tag not found');
    }
    return svg;
}

function changeTurns() {

    // Switch the turn
    if (currentPlayer == player1Name) {
        currentPlayer = player2Name;
    } else {
        currentPlayer = player1Name;
    }

    // Update who's turn it is
    $('#turnDisplay').text("It's now " + currentPlayer + " turn");
}

function updateBallDisplay(FirstBallNum){
    var text1, text2;

    if (FirstBallNum >= 1 && FirstBallNum <= 7 && currentPlayer == player1Name) {
        //set the globel var
        player1Balls = "low";
        player2Balls = "high";

        //set the text
        text1 = "low - Balls 1-7";
        text2 = "high - Balls 9-15";
    } else {
        //set the globel var
        player1Balls = "low";
        player2Balls = "high";

        //set the text
        text2 = "low - Balls 1-7";
        text1 = "high - Balls 9-15";
    }

    $('#player1').text(`${player1Name} - ${text1}`);
    $('#player2').text(`${player2Name} - ${text2}`);
}

//when ball is pocketed
function updateGameState(ballNum) {
    
    //if its the first ball pocketed - assign high and low
    if(allBalls.length() == 15 && ballNum != 0){
        updateBallDisplay(ballNum);
    }

    //check to see if cue ball goes in
    if (ballNum == 0) {
        //reset the ball to the start
        //find the ball
        const ballElement = document.getElementById(`ball0`);

        if (!ballElement) {
            console.error(`Cound not find Ball number 0`);
            return;
        }

        //set the x and y attributes
        ballElement.setAttribute('cx', 675);
        ballElement.setAttribute('cy', 2025);

        console.log(`Ball 0 moved to (675, 2025)`);

        //MIGHT NEED OTHER LOGIC AFTER

    }else{
        //remove from list
        allBalls.remove(ballNum);
    }

    checkForWinner(ballNum);
}

function checkForWinner(ballNum) {

    //check to see if 8 ball in and the current player and if low or high
    if (ballNum == 8 && currentPlayer == player1Name) {

        //check global list to see if all balls
        if(allBalls.some(ball => ball >= 1 && ball <= 7) && player1Balls == "low"){
            announceWinner(player1Name);

        }else if(allBalls.some(ball => ball >= 9 && ball <= 15) && player1Balls == "high"){
            announceWinner(player1Name);
        }else{
            announceWinner(player2Name);
        }
    
    } else if (ballNum == 8 && currentPlayer == player2Name) {

        //check global list to see if all balls
        if(allBalls.some(ball => ball >= 1 && ball <= 7) && player2Balls == "low"){
            announceWinner(player2Name);

        }else if(allBalls.some(ball => ball >= 9 && ball <= 15) && player2Balls == "high"){
            announceWinner(player2Name);
        }else{
            //still have balls on pool table
            announceWinner(player1Name);
        }
    }
}

function announceWinner(winnerName) {
    alert(winnerName + " wins the game!");
}