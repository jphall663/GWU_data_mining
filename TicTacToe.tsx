import React, { useState, useEffect, useCallback } from 'react';

// Helper function (can be outside the component)
function calculateWinner(squares: Array<string | null>): string | null {
  const lines = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
    [0, 4, 8], [2, 4, 6],             // diagonals
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}

// Computer move logic function
function makeComputerMove(currentBoard: Array<string | null>): number {
  const computerMark = 'O';
  const playerMark = 'X';

  // Check for winning move for computer
  for (let i = 0; i < 9; i++) {
    if (!currentBoard[i]) {
      const tempBoard = [...currentBoard];
      tempBoard[i] = computerMark;
      if (calculateWinner(tempBoard) === computerMark) {
        return i;
      }
    }
  }

  // Check for blocking move against player
  for (let i = 0; i < 9; i++) {
    if (!currentBoard[i]) {
      const tempBoard = [...currentBoard];
      tempBoard[i] = playerMark;
      if (calculateWinner(tempBoard) === playerMark) {
        return i;
      }
    }
  }

  // Try center
  if (!currentBoard[4]) return 4;

  // Try corners (random order for variety)
  const corners = [0, 2, 6, 8].sort(() => Math.random() - 0.5);
  for (const corner of corners) {
    if (!currentBoard[corner]) return corner;
  }

  // Try sides (random order for variety)
  const sides = [1, 3, 5, 7].sort(() => Math.random() - 0.5);
  for (const side of sides) {
    if (!currentBoard[side]) return side;
  }
  
  // Fallback: find any available spot
  const availableSpots = currentBoard.map((val, idx) => val === null ? idx : -1).filter(idx => idx !== -1);
  if (availableSpots.length > 0) return availableSpots[Math.floor(Math.random() * availableSpots.length)];

  return -1; // Should not happen
}


const TicTacToe: React.FC = () => {
  const [board, setBoard] = useState<Array<string | null>>(Array(9).fill(null));
  const [xIsNext, setXIsNext] = useState<boolean>(true); // Player X starts
  const [gameMode, setGameMode] = useState<string>(''); // '', 'pvp', 'pvc'

  const cellStyle: React.CSSProperties = {
    width: '100px',
    height: '100px',
    border: '2px solid black',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    fontSize: '3em',
    cursor: 'pointer',
  };

  const boardStyle: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 100px)',
    gridGap: '5px',
    width: '310px', 
    margin: '20px auto',
  };

  const statusStyle: React.CSSProperties = {
    marginBottom: '10px',
    fontSize: '1.5em',
    textAlign: 'center',
  };
  
  const gameContainerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    fontFamily: 'Arial, sans-serif',
  };

  const buttonStyle: React.CSSProperties = {
    marginTop: '20px',
    padding: '10px 15px',
    fontSize: '1em',
    cursor: 'pointer',
    marginRight: '10px', // Added for spacing between mode buttons
  };
  
  const modeSelectionContainerStyle: React.CSSProperties = {
    margin: '20px',
    textAlign: 'center',
  };

  const resetGameForModeSelection = () => {
    setBoard(Array(9).fill(null));
    setXIsNext(true); // Player X always starts
    // gameMode is set by the buttons themselves
  };

  const handlePlayAgain = () => {
    setBoard(Array(9).fill(null));
    setXIsNext(true); // Player X always starts
    // gameMode persists
  };
  
  // Memoized handleCellClick to ensure stability for useEffect
  const handleCellClick = useCallback((index: number) => {
    if (!gameMode || calculateWinner(board) || board[index]) {
      return;
    }

    // In PVC, if it's O's turn, human clicks should be ignored.
    // The useEffect will handle O's move.
    if (gameMode === 'pvc' && !xIsNext) {
        return;
    }

    const newBoard = [...board];
    newBoard[index] = xIsNext ? 'X' : 'O';
    setBoard(newBoard);
    setXIsNext(!xIsNext);
  }, [board, xIsNext, gameMode]);


  useEffect(() => {
    if (gameMode === 'pvc' && !xIsNext && !calculateWinner(board) && board.some(cell => cell === null)) {
      const computerMove = makeComputerMove(board);
      if (computerMove !== -1 && !board[computerMove]) {
        // Using a timeout to give a slight delay for UX, makes it feel more like an opponent
        setTimeout(() => {
            handleCellClick(computerMove);
        }, 500);
      }
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [xIsNext, board, gameMode, handleCellClick]); // handleCellClick is now memoized

  const winner = calculateWinner(board);
  const isDraw = !winner && board.every(cell => cell !== null);
  let gameStatus;

  if (winner) {
    gameStatus = `Winner: ${winner}`;
  } else if (isDraw) {
    gameStatus = "It's a Draw!";
  } else if (gameMode) { // Only show next player if a mode is selected
    gameStatus = `Next Player: ${xIsNext ? 'X' : 'O'}`;
  } else {
    gameStatus = "Select a game mode to start!"
  }

  return (
    <div style={gameContainerStyle}>
      <h1>Juego de Michi del Prof. Ernesto Cancho</h1>
      
      {!gameMode && (
        <div style={modeSelectionContainerStyle}>
          <h2>Select Game Mode</h2>
          <button 
            onClick={() => { setGameMode('pvp'); resetGameForModeSelection(); }} 
            style={buttonStyle}
          >
            Player vs Player
          </button>
          <button 
            onClick={() => { setGameMode('pvc'); resetGameForModeSelection(); }} 
            style={buttonStyle}
          >
            Player vs Computer
          </button>
        </div>
      )}

      {gameMode && (
        <>
          <div style={statusStyle}>
            {gameStatus}
          </div>
          <div style={boardStyle}>
            {board.map((cell, index) => (
              <div
                key={index}
                style={cellStyle}
                onClick={() => handleCellClick(index)}
              >
                {cell}
              </div>
            ))}
          </div>
          {(winner || isDraw) && (
            <button onClick={handlePlayAgain} style={buttonStyle}>
              Play Again
            </button>
          )}
        </>
      )}
    </div>
  );
};

export default TicTacToe;
