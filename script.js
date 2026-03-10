let userScore = 0;
let compScore = 0;

choices = document.querySelectorAll(".choice");

const userScorePara = document.querySelector("#user-score");
const compScorePara = document.querySelector("#comp-score");
const msg = document.querySelector("#msg");

drawGame = ()=>{
    msg.innerText = "Game is draw, play again";
    msg.style.backgroundColor ="#89bceb";
}

getCompChoice = ()=>{
    const options = ["rock","paper","scissor"];
    const randomIndex = Math.floor(Math.random()*3);
    return options[randomIndex];
}

    const showWinner =(userWin, userChoice, compChoice)=>{
        if(userWin){
            userScore++;
            userScorePara.innerText = userScore;
            msg.innerText = `You win! Your ${userChoice} beats ${compChoice}`;
            msg.style.backgroundColor = "#8beb89";
        } else{
            compScore++;
             compScorePara.innerText = compScore;
             msg.innerText = `You lost. ${compChoice} beats your ${userChoice}`;
             msg.style.backgroundColor = "#ea7d7d";
        }
    };

const playGame = (userChoice)=>{
    compChoice = getCompChoice();

    if(userChoice === compChoice){
        drawGame();
    }
    else{
        let userWin = true;
    if (userChoice === "rock") {
      //scissors, paper
      userWin = compChoice === "paper" ? false : true;
    } else if (userChoice === "paper") {
      //rock, scissors
      userWin = compChoice === "scissors" ? false : true;
    } else {
      //rock, paper
      userWin = compChoice === "rock" ? false : true;
    }
    showWinner(userWin, userChoice, compChoice);
    }
};


choices.forEach((choice)=>{
    choice.addEventListener("click",()=>{
    const userChoice = choice.getAttribute("id");
    playGame(userChoice);
    });
});
