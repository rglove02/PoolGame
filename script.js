var currentPlayer;
var player1Name;
var player2Name;
var gameName;

//tells if low or high
var player1Balls;
var player2Balls;

//list of balls on the table
var allBalls = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15];
var shotBallsBefore = [];
var shotPlayer = null;

// Colours for scoreboard balls
var DISPLAY_BALL_COLOURS = {
    1: "#F4D03F",
    2: "#2463D4",
    3: "#D62828",
    4: "#7B2C91",
    5: "#F28C28",
    6: "#25823B",
    7: "#7B3F26",

    9: "#F4D03F",
    10: "#2463D4",
    11: "#D62828",
    12: "#7B2C91",
    13: "#F28C28",
    14: "#25823B",
    15: "#7B3F26"
};

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

        // low/high assignment
        player1Balls = localStorage.getItem('player1Balls');
        player2Balls = localStorage.getItem('player2Balls');

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

        // mouse down event on the SVG container
        $('#svgInfo').on('mousedown', function () {
            isMouseDown = true; // Set flag when mouse button is pressed
            showLine(event); // Show the line where the mouse is pressed
        });

        // mouse up event on the entire document to handle button release anywhere
        $(document).on('mouseup', function () {
            if (isMouseDown && isMouseOverSVG) { // Ensure the mouse was down and over the SVG for a "shot"
                shotit(event);
            }
            isMouseDown = false; // Clear flag when mouse button is released
            hideLine(); // Hide the line
        });

        // modify the existing mousemove on the div to check if the mouse is over the SVG
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

// send to server
function sendNames() {

    initalizePlayers()

    // send names to server
    const data = {
        player1: player1Name,
        player2: player2Name,
        game: gameName
    };

    // send names to server
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

    // retrieve names from local storage
    player1Name = $("#player1Name").val()
    player2Name = $("#player2Name").val()
    gameName = $("#gameName").val()

    // randomly decide who goes first
    currentPlayer = Math.random() < 0.5 ? player1Name : player2Name;

    // reset game scoring information
    allBalls = [
        1, 2, 3, 4, 5, 6, 7,
        9, 10, 11, 12, 13, 14, 15
    ];

    player1Balls = null;
    player2Balls = null;

    // add to storage for when redirect to pool.html
    localStorage.setItem('player1Name', player1Name);
    localStorage.setItem('player2Name', player2Name);
    localStorage.setItem('gameName', gameName);
    localStorage.setItem('currentPlayer', currentPlayer);

    // allBalls is an array, we need to stringify it
    localStorage.setItem('allBalls', JSON.stringify(allBalls));

    // remove group assignment from old game
    localStorage.removeItem('player1Balls');
    localStorage.removeItem('player2Balls');

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

// update scoreboard HTML that is in pool.html
function lowHighBallDisplay(){
    // $('#ballnumInfo').append();
    // $('#ballnumInfo').append();

    if (!player1Balls || !player2Balls) {

        $('#openTableCard').show();
        $('#playerScoreBoard').hide();

        return;
    }

    $('#openTableCard').hide();
    $('#playerScoreBoard').css('display', 'flex');

    // player names
    $('#scorePlayer1Name').text(player1Name);
    $('#scorePlayer2Name').text(player2Name);

    // group names
    if (player1Balls == "low") {
        $('#scorePlayer1Group').text("SOLIDS");
    } else {
        $('#scorePlayer1Group').text("STRIPES");
    }

    if (player2Balls == "low") {
        $('#scorePlayer2Group').text("SOLIDS");
    } else {
        $('#scorePlayer2Group').text("STRIPES");
    }

    // group badge colours
    $('#scorePlayer1Group')
        .removeClass('low high')
        .addClass(player1Balls);

    $('#scorePlayer2Group')
        .removeClass('low high')
        .addClass(player2Balls);

    // show current player
    $('#player1ScoreCard').removeClass('active-player');
    $('#player2ScoreCard').removeClass('active-player');

    if (currentPlayer == player1Name) {
        $('#player1ScoreCard').addClass('active-player');
    } else {
        $('#player2ScoreCard').addClass('active-player');
    }

    // remaining balls
    const player1Remaining =
        ballsRemainingForGroup(player1Balls);

    const player2Remaining =
        ballsRemainingForGroup(player2Balls);


    setScoreBallSlots(
        "player1ScoreBall",
        player1Remaining
    );

    setScoreBallSlots(
        "player2ScoreBall",
        player2Remaining
    );


    // message once all group balls are gone
    if (player1Remaining.length == 0) {
        $('#player1Cleared').show();
    } else {
        $('#player1Cleared').hide();
    }

    if (player2Remaining.length == 0) {
        $('#player2Cleared').show();
    } else {
        $('#player2Cleared').hide();
    }
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


    // ============================================================
    // ADDED: remember balls before shot
    // ============================================================

    shotBallsBefore =
        getBallNumbersFromElement(svgElement);

    shotPlayer = currentPlayer;


    //create post request and pass values
    $.ajax({
        type: "POST",
        url: "http://localhost:52174/process-shot",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (result) {
            // Handle successful response
            console.log("Shot processed:", result);

            const SVGDiv = $('#svgInfo');
            const tableSVG = result.tableSVG;


            // ====================================================
            // ADDED: see which balls disappeared
            // ====================================================

            const pocketedBalls =
                findPocketedBalls(
                    shotBallsBefore,
                    tableSVG
                );

            console.log(
                "Pocketed balls:",
                pocketedBalls
            );


            //loop through and replace svg
            for (let i = 0; i < tableSVG.length; i++) {
                setTimeout(function () {
                    SVGDiv.html(tableSVG[i]);
                }, i * 10);
            }


            /*
            =======================================================
            ORIGINAL TURN CODE - KEPT BUT COMMENTED OUT

            This always changed the player after a shot.
            New scoring code below decides if the same player
            gets another turn.
            =======================================================

            setTimeout(function () {
                changeTurns();
            }, tableSVG.length * 10);

            //change turns
            changeTurns();

            */


            // ====================================================
            // ADDED: process score after animation
            // ====================================================

            setTimeout(function () {

                processShotScoring(
                    pocketedBalls,
                    shotPlayer
                );

            }, tableSVG.length * 10 + 20);
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


    // ============================================================
    // ADDED: remember and display new turn
    // ============================================================

    localStorage.setItem(
        'currentPlayer',
        currentPlayer
    );

    lowHighBallDisplay();
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



// ================================================================
// ADDED FUNCTIONS BELOW
//
// Original functions above remain in the file.
// ================================================================


// Return all ball numbers currently in the SVG
function getBallNumbersFromElement(svgRoot) {

    const ballNumbers = [];

    if (!svgRoot) {
        return ballNumbers;
    }

    svgRoot
        .querySelectorAll('[id^="ball"]')
        .forEach(function (ballElement) {

            const match =
                ballElement.id.match(
                    /^ball(\d+)$/
                );

            if (match) {

                ballNumbers.push(
                    parseInt(match[1])
                );
            }
        });

    return [...new Set(ballNumbers)];
}


// Get ball numbers from an SVG string returned by Python
function getBallNumbersFromSVGString(svgString) {

    const parser = new DOMParser();

    const svgDocument =
        parser.parseFromString(
            svgString,
            "image/svg+xml"
        );

    return getBallNumbersFromElement(
        svgDocument
    );
}


// Find which balls disappeared during the shot
function findPocketedBalls(
    ballsBeforeShot,
    tableSVG
) {

    let previousBalls =
        ballsBeforeShot.slice();

    const pocketedBalls = [];


    for (const frame of tableSVG) {

        const currentBalls =
            getBallNumbersFromSVGString(
                frame
            );


        for (const ballNum of previousBalls) {

            if (
                !currentBalls.includes(ballNum) &&
                !pocketedBalls.includes(ballNum)
            ) {

                pocketedBalls.push(
                    ballNum
                );
            }
        }


        previousBalls =
            currentBalls;
    }


    return pocketedBalls;
}


// Determine which group a ball belongs to
function groupForBall(ballNum) {

    // solids / low
    if (ballNum >= 1 && ballNum <= 7) {
        return "low";
    }

    // stripes / high
    if (ballNum >= 9 && ballNum <= 15) {
        return "high";
    }
    return null;
}

// Return a player's group
function getPlayerGroup(playerName) {
    if (playerName == player1Name) {
        return player1Balls;
    }

    if (playerName == player2Name) {
        return player2Balls;
    }
    return null;
}

// Get remaining balls for solids or stripes
function ballsRemainingForGroup(group) {
    if (group == "low") {
        return allBalls.filter(
            ball =>
                ball >= 1 &&
                ball <= 7
        );
    }

    if (group == "high") {
        return allBalls.filter(
            ball =>
                ball >= 9 &&
                ball <= 15
        );
    }
    return [];
}

// Assign solids/stripes after first valid ball goes in
function assignGroups(firstBallNum, shooter) {

    // already assigned
    if (player1Balls ||
        player2Balls
    ) {

        return;
    }

    const shooterGroup =
        groupForBall(
            firstBallNum
        );

    if (!shooterGroup) {
        return;
    }

    const otherGroup =
        shooterGroup == "low"
            ? "high"
            : "low";

    if (shooter == player1Name) {

        player1Balls =
            shooterGroup;

        player2Balls =
            otherGroup;

    } else {

        player2Balls =
            shooterGroup;

        player1Balls =
            otherGroup;
    }

    localStorage.setItem(
        'player1Balls',
        player1Balls
    );

    localStorage.setItem(
        'player2Balls',
        player2Balls
    );

    lowHighBallDisplay();
}

// See if a ball belongs to a particular player
function playerOwnsBall(
    playerName,
    ballNum
) {

    const group =
        getPlayerGroup(
            playerName
        );


    return (
        groupForBall(ballNum)
        ==
        group
    );
}

// Update the seven little ball slots in pool.html
function setScoreBallSlots(
    idPrefix,
    balls
) {

    for (let i = 0; i < 7; i++) {

        const slot =
            document.getElementById(
                idPrefix + i
            );


        if (!slot) {
            continue;
        }


        // reset slot
        slot.classList.remove(
            'score-solid',
            'score-striped'
        );

        slot.removeAttribute(
            'data-ball-number'
        );


        // no ball for this slot
        if (i >= balls.length) {

            slot.style.display =
                'none';

            continue;
        }


        const ballNum =
            balls[i];


        const colour =
            DISPLAY_BALL_COLOURS[
                ballNum
            ];


        slot.style.setProperty(
            '--ball-colour',
            colour
        );


        slot.setAttribute(
            'data-ball-number',
            ballNum
        );


        if (
            ballNum >= 1 &&
            ballNum <= 7
        ) {

            slot.classList.add(
                'score-solid'
            );

        } else {

            slot.classList.add(
                'score-striped'
            );
        }


        slot.style.display =
            'inline-flex';
    }
}


// Process all scoring and turn logic after one shot
function processShotScoring(
    pocketedBalls,
    shooter
) {

    // If nobody has solids/stripes yet,
    // first valid object ball assigns them.
    if (
        !player1Balls &&
        !player2Balls
    ) {

        const firstGroupBall =
            pocketedBalls.find(
                function (ballNum) {

                    return (
                        groupForBall(
                            ballNum
                        )
                        !=
                        null
                    );
                }
            );


        if (
            firstGroupBall
            !==
            undefined
        ) {

            assignGroups(
                firstGroupBall,
                shooter
            );
        }
    }


    // Remove pocketed solids/stripes
    // from the remaining-ball list
    for (
        const ballNum
        of pocketedBalls
    ) {

        if (
            groupForBall(
                ballNum
            )
            !=
            null
        ) {

            allBalls =
                allBalls.filter(
                    ball =>
                        ball != ballNum
                );
        }
    }


    localStorage.setItem(
        'allBalls',
        JSON.stringify(allBalls)
    );


    lowHighBallDisplay();


    const cueBallPocketed =
        pocketedBalls.includes(0);


    const eightBallPocketed =
        pocketedBalls.includes(8);


    // 8-ball was pocketed
    if (eightBallPocketed) {

        const shooterGroup =
            getPlayerGroup(
                shooter
            );


        const ballsLeft =
            ballsRemainingForGroup(
                shooterGroup
            );


        // shooter cleared their group first
        if (
            shooterGroup != null &&
            ballsLeft.length == 0 &&
            !cueBallPocketed
        ) {

            announceWinner(
                shooter
            );

        } else {

            // 8 ball too early or scratch on 8
            if (
                shooter
                ==
                player1Name
            ) {

                announceWinner(
                    player2Name
                );

            } else {

                announceWinner(
                    player1Name
                );
            }
        }


        return;
    }


    // cue ball pocketed
    if (cueBallPocketed) {

        changeTurns();

        return;
    }


    // Did shooter pocket at least one
    // ball belonging to their group?
    const pocketedOwnBall =
        pocketedBalls.some(
            function (ballNum) {

                return playerOwnsBall(
                    shooter,
                    ballNum
                );
            }
        );


    if (pocketedOwnBall) {

        // same player gets another turn
        currentPlayer =
            shooter;


        localStorage.setItem(
            'currentPlayer',
            currentPlayer
        );


        $('#turnDisplay').text(
            "It's still " +
            currentPlayer +
            " turn"
        );


        lowHighBallDisplay();

    } else {

        // no own ball pocketed
        changeTurns();
    }
}