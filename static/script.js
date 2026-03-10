let userScore = 0;
let compScore = 0;

const choices = document.querySelectorAll(".choice");
const userScorePara = document.querySelector("#user-score");
const compScorePara = document.querySelector("#comp-score");
const msg = document.querySelector("#msg");

// Function to send game result to backend
async function saveGameResult(userChoice, computerChoice, result) {
    try {
        const response = await fetch('/api/game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_choice: userChoice,
                computer_choice: computerChoice,
                result: result
            })
        });
        if (!response.ok) {
            console.error('Failed to save game');
        }
    } catch (error) {
        console.error('Error saving game:', error);
    }
}

const drawGame = (userChoice, compChoice) => {
    msg.innerText = "Game is draw, play again";
    msg.style.backgroundColor = "#89bceb";
    saveGameResult(userChoice, compChoice, 'tie');
};

const getCompChoice = () => {
    const options = ["rock", "paper", "scissor"];
    const randomIndex = Math.floor(Math.random() * 3);
    return options[randomIndex];
};

const showWinner = (userWin, userChoice, compChoice) => {
    if (userWin) {
        userScore++;
        userScorePara.innerText = userScore;
        msg.innerText = `You win! Your ${userChoice} beats ${compChoice}`;
        msg.style.backgroundColor = "#8beb89";
        saveGameResult(userChoice, compChoice, 'win');
    } else {
        compScore++;
        compScorePara.innerText = compScore;
        msg.innerText = `You lost. ${compChoice} beats your ${userChoice}`;
        msg.style.backgroundColor = "#ea7d7d";
        saveGameResult(userChoice, compChoice, 'loss');
    }
};

const playGame = (userChoice) => {
    const compChoice = getCompChoice();

    if (userChoice === compChoice) {
        drawGame(userChoice, compChoice);
    } else {
        let userWin = true;
        if (userChoice === "rock") {
            userWin = compChoice === "paper" ? false : true;
        } else if (userChoice === "paper") {
            userWin = compChoice === "scissor" ? false : true;
        } else { // scissor
            userWin = compChoice === "rock" ? false : true;
        }
        showWinner(userWin, userChoice, compChoice);
    }
};

choices.forEach((choice) => {
    choice.addEventListener("click", () => {
        const userChoice = choice.getAttribute("id");
        playGame(userChoice);
    });
});

// Add button to view history
const historyButton = document.createElement('button');
historyButton.innerText = 'View History';
historyButton.style.margin = '20px';
historyButton.style.padding = '10px 20px';
historyButton.style.fontSize = '1.2rem';
historyButton.style.cursor = 'pointer';
document.body.appendChild(historyButton);

historyButton.addEventListener('click', async () => {
    const response = await fetch('/api/history');
    const history = await response.json();
    displayHistory(history);
});

function displayHistory(history) {
    // Create a modal or simple overlay
    const existingModal = document.getElementById('history-modal');
    if (existingModal) existingModal.remove();

    const modal = document.createElement('div');
    modal.id = 'history-modal';
    modal.style.position = 'fixed';
    modal.style.top = '50%';
    modal.style.left = '50%';
    modal.style.transform = 'translate(-50%, -50%)';
    modal.style.backgroundColor = 'white';
    modal.style.padding = '20px';
    modal.style.border = '2px solid black';
    modal.style.zIndex = '1000';
    modal.style.maxHeight = '80%';
    modal.style.overflowY = 'auto';
    modal.style.minWidth = '300px';

    const closeBtn = document.createElement('button');
    closeBtn.innerText = 'Close';
    closeBtn.style.marginBottom = '10px';
    closeBtn.onclick = () => modal.remove();

    const title = document.createElement('h3');
    title.innerText = 'Game History';

    const list = document.createElement('ul');
    list.style.listStyle = 'none';
    list.style.padding = '0';

    history.forEach(round => {
        const item = document.createElement('li');
        item.style.margin = '10px 0';
        item.style.padding = '10px';
        item.style.border = '1px solid #ccc';
        item.innerHTML = `
            <strong>${round.timestamp}</strong><br>
            You: ${round.user_choice} | Computer: ${round.computer_choice}<br>
            Result: <span style="color: ${round.result === 'win' ? 'green' : (round.result === 'loss' ? 'red' : 'orange')}">${round.result}</span>
            <button class="delete-btn" data-id="${round.id}" style="margin-left: 10px;">Delete</button>
        `;
        list.appendChild(item);
    });

    // Add delete all button
    const deleteAllBtn = document.createElement('button');
    deleteAllBtn.innerText = 'Delete All History';
    deleteAllBtn.style.marginTop = '10px';
    deleteAllBtn.onclick = async () => {
        if (confirm('Delete all history?')) {
            await fetch('/api/history', { method: 'DELETE' });
            modal.remove();
            alert('All history deleted');
        }
    };

    modal.appendChild(closeBtn);
    modal.appendChild(title);
    modal.appendChild(list);
    modal.appendChild(deleteAllBtn);
    document.body.appendChild(modal);

    // Add event listeners for delete buttons
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation();
            const id = btn.dataset.id;
            if (confirm('Delete this record?')) {
                await fetch(`/api/game/${id}`, { method: 'DELETE' });
                btn.parentElement.remove();
            }
        });
    });
}