import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Trophy, Calendar, Flame, X, Check, RefreshCw, HelpCircle } from 'lucide-react';
import './KenKenGame.css';

const KenKenGame = ({ onClose, pillarName }) => {
    const [gameState, setGameState] = useState(null);
    const [selectedCell, setSelectedCell] = useState(null);
    const [userGrid, setUserGrid] = useState([]);
    const [errors, setErrors] = useState([]);
    const [isComplete, setIsComplete] = useState(false);
    const [streak, setStreak] = useState(0);
    const [lastPlayed, setLastPlayed] = useState(null);
    const [showHints, setShowHints] = useState(false);
    const [focusedCell, setFocusedCell] = useState(null);
    const [currentHint, setCurrentHint] = useState(null);

    // Handle keyboard input
    useEffect(() => {
        const handleKeyPress = (e) => {
            if (isComplete) return;

            const key = e.key;
            if (key >= '1' && key <= String(gameState?.size || 4)) {
                if (focusedCell) {
                    handleCellInput(focusedCell.row, focusedCell.col, parseInt(key));
                }
            } else if (key === 'Backspace' || key === 'Delete' || key === '0') {
                if (focusedCell) {
                    handleCellInput(focusedCell.row, focusedCell.col, 0);
                }
            } else if (key === 'ArrowUp' || key === 'ArrowDown' || key === 'ArrowLeft' || key === 'ArrowRight') {
                e.preventDefault();
                if (focusedCell && gameState) {
                    let { row, col } = focusedCell;
                    if (key === 'ArrowUp') row = Math.max(0, row - 1);
                    if (key === 'ArrowDown') row = Math.min(gameState.size - 1, row + 1);
                    if (key === 'ArrowLeft') col = Math.max(0, col - 1);
                    if (key === 'ArrowRight') col = Math.min(gameState.size - 1, col + 1);
                    setFocusedCell({ row, col });
                    setSelectedCell({ row, col });
                }
            }
        };

        window.addEventListener('keydown', handleKeyPress);
        return () => window.removeEventListener('keydown', handleKeyPress);
    }, [focusedCell, gameState, isComplete]);

    // Generate daily seed based on date
    const getDailySeed = () => {
        const today = new Date();
        return `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}-${pillarName}`;
    };

    // Seeded random number generator
    const seededRandom = (seed) => {
        const x = Math.sin(seed) * 10000;
        return x - Math.floor(x);
    };

    // Generate KenKen puzzle based on daily seed
    const generateKenKenPuzzle = () => {
        const seed = getDailySeed();
        let hashCode = 0;
        for (let i = 0; i < seed.length; i++) {
            hashCode = seed.charCodeAt(i) + ((hashCode << 5) - hashCode);
        }

        // Generate different grid sizes daily: 3x3, 4x4, 5x5, or 6x6
        const gridSizes = [3, 4, 5, 6];
        const sizeIndex = Math.abs(hashCode) % gridSizes.length;
        const size = gridSizes[sizeIndex];

        const solution = generateSolution(size, hashCode);
        const cages = generateCages(solution, hashCode);

        return {
            size,
            solution,
            cages,
            seed
        };
    };

    // Generate valid solution grid
    const generateSolution = (size, seed) => {
        const grid = [];
        const offset = Math.floor(seededRandom(seed) * size);

        for (let row = 0; row < size; row++) {
            grid[row] = [];
            for (let col = 0; col < size; col++) {
                grid[row][col] = ((row + col + offset) % size) + 1;
            }
        }

        // Shuffle rows and columns based on seed
        for (let i = 0; i < size; i++) {
            const swapRow = Math.floor(seededRandom(seed + i) * size);
            [grid[i], grid[swapRow]] = [grid[swapRow], grid[i]];
        }

        return grid;
    };

    // Generate cages with operations
    const generateCages = (solution, seed) => {
        const size = solution.length;
        const cages = [];
        const used = Array(size).fill(null).map(() => Array(size).fill(false));
        const operations = ['+', '-', '×', '÷'];

        let cageId = 0;
        for (let row = 0; row < size; row++) {
            for (let col = 0; col < size; col++) {
                if (!used[row][col]) {
                    const cage = {
                        id: cageId++,
                        cells: [[row, col]],
                        operation: null,
                        target: solution[row][col]
                    };
                    used[row][col] = true;

                    // Try to expand cage
                    const expansions = Math.floor(seededRandom(seed + cageId * 100) * 2) + 1;
                    for (let i = 0; i < expansions; i++) {
                        const lastCell = cage.cells[cage.cells.length - 1];
                        const [r, c] = lastCell;
                        const directions = [];

                        if (r + 1 < size && !used[r + 1][c]) directions.push([r + 1, c]);
                        if (c + 1 < size && !used[r][c + 1]) directions.push([r, c + 1]);

                        if (directions.length > 0) {
                            const dir = directions[Math.floor(seededRandom(seed + cageId * 200 + i) * directions.length)];
                            cage.cells.push(dir);
                            used[dir[0]][dir[1]] = true;
                        } else {
                            break;
                        }
                    }

                    // Calculate target and operation
                    if (cage.cells.length === 1) {
                        cage.target = solution[cage.cells[0][0]][cage.cells[0][1]];
                        cage.operation = null;
                    } else {
                        const values = cage.cells.map(([r, c]) => solution[r][c]);
                        const opIndex = Math.floor(seededRandom(seed + cageId * 300) * operations.length);
                        cage.operation = operations[opIndex];

                        switch (cage.operation) {
                            case '+':
                                cage.target = values.reduce((a, b) => a + b, 0);
                                break;
                            case '-':
                                cage.target = Math.abs(values[0] - values[1]);
                                break;
                            case '×':
                                cage.target = values.reduce((a, b) => a * b, 1);
                                break;
                            case '÷':
                                cage.target = Math.max(...values) / Math.min(...values);
                                if (!Number.isInteger(cage.target)) {
                                    cage.operation = '+';
                                    cage.target = values.reduce((a, b) => a + b, 0);
                                }
                                break;
                        }
                    }

                    cages.push(cage);
                }
            }
        }

        return cages;
    };

    // Initialize game
    useEffect(() => {
        const puzzle = generateKenKenPuzzle();
        setGameState(puzzle);
        setUserGrid(Array(puzzle.size).fill(null).map(() => Array(puzzle.size).fill(0)));

        // Load streak from localStorage
        const savedData = JSON.parse(localStorage.getItem(`kenken-${pillarName}`) || '{}');
        setStreak(savedData.streak || 0);
        setLastPlayed(savedData.lastPlayed || null);
    }, [pillarName]);

    // Handle cell input with validation
    const handleCellInput = (row, col, value) => {
        if (!gameState) return;

        const numValue = parseInt(value);

        // Allow empty (0) or valid numbers within range
        if (value === '' || value === '0' || !numValue) {
            const newGrid = [...userGrid];
            newGrid[row][col] = 0;
            setUserGrid(newGrid);
            setErrors([]);
            return;
        }

        // Validate number is within allowed range (1 to size)
        if (numValue >= 1 && numValue <= gameState.size) {
            const newGrid = [...userGrid];
            newGrid[row][col] = numValue;
            setUserGrid(newGrid);
            setErrors([]);
        }
        // If invalid, don't update and optionally show error
    };

    // Check solution
    const checkSolution = () => {
        if (!gameState) return;

        const newErrors = [];

        // Check if all cells are filled
        for (let row = 0; row < gameState.size; row++) {
            for (let col = 0; col < gameState.size; col++) {
                if (userGrid[row][col] === 0) {
                    newErrors.push(`Cell (${row + 1}, ${col + 1}) is empty`);
                }
            }
        }

        // Check rows for duplicates
        for (let row = 0; row < gameState.size; row++) {
            const rowValues = userGrid[row];
            const uniqueValues = new Set(rowValues.filter(v => v !== 0));
            if (uniqueValues.size !== rowValues.filter(v => v !== 0).length) {
                newErrors.push(`Row ${row + 1} has duplicate values`);
            }
        }

        // Check columns for duplicates
        for (let col = 0; col < gameState.size; col++) {
            const colValues = userGrid.map(row => row[col]);
            const uniqueValues = new Set(colValues.filter(v => v !== 0));
            if (uniqueValues.size !== colValues.filter(v => v !== 0).length) {
                newErrors.push(`Column ${col + 1} has duplicate values`);
            }
        }

        // Check cages
        gameState.cages.forEach(cage => {
            const values = cage.cells.map(([r, c]) => userGrid[r][c]);
            if (values.some(v => v === 0)) return;

            let result;
            if (cage.operation === null) {
                result = values[0];
            } else {
                switch (cage.operation) {
                    case '+':
                        result = values.reduce((a, b) => a + b, 0);
                        break;
                    case '-':
                        result = Math.abs(values[0] - values[1]);
                        break;
                    case '×':
                        result = values.reduce((a, b) => a * b, 1);
                        break;
                    case '÷':
                        result = Math.max(...values) / Math.min(...values);
                        break;
                }
            }

            if (result !== cage.target) {
                newErrors.push(`Cage with target ${cage.target}${cage.operation || ''} is incorrect`);
            }
        });

        setErrors(newErrors);

        if (newErrors.length === 0) {
            setIsComplete(true);
            updateStreak();
        }
    };

    // Update streak with proper daily tracking
    const updateStreak = () => {
        const today = new Date().toDateString();
        const savedData = JSON.parse(localStorage.getItem(`kenken-${pillarName}`) || '{}');

        // If already completed today, don't update streak
        if (savedData.lastPlayed === today) {
            setStreak(savedData.streak || 1);
            return;
        }

        let newStreak = 1;
        if (savedData.lastPlayed) {
            const lastDate = new Date(savedData.lastPlayed);
            const todayDate = new Date();

            // Calculate days difference properly
            lastDate.setHours(0, 0, 0, 0);
            todayDate.setHours(0, 0, 0, 0);
            const daysDiff = Math.floor((todayDate - lastDate) / (1000 * 60 * 60 * 24));

            if (daysDiff === 1) {
                // Consecutive day - increment streak
                newStreak = (savedData.streak || 0) + 1;
            } else if (daysDiff > 1) {
                // Gap in days - reset streak
                newStreak = 1;
            }
        }

        setStreak(newStreak);
        localStorage.setItem(`kenken-${pillarName}`, JSON.stringify({
            streak: newStreak,
            lastPlayed: today
        }));
    };

    // Reset puzzle
    const resetPuzzle = () => {
        if (!gameState) return;
        setUserGrid(Array(gameState.size).fill(null).map(() => Array(gameState.size).fill(0)));
        setErrors([]);
        setIsComplete(false);
        setCurrentHint(null);
    };

    // Generate intelligent hint using actual solution
    const generateHint = () => {
        if (!gameState || !gameState.solution) return;

        // Strategy 1: Find empty cells and provide solution value
        for (let row = 0; row < gameState.size; row++) {
            for (let col = 0; col < gameState.size; col++) {
                if (userGrid[row][col] === 0) {
                    const correctValue = gameState.solution[row][col];
                    const cage = getCageForCell(row, col);
                    setCurrentHint(`Cell (${row + 1}, ${col + 1}) should be ${correctValue} (Cage: ${cage.target}${cage.operation || ''})`);
                    setFocusedCell({ row, col });
                    setSelectedCell({ row, col });
                    return;
                }
            }
        }

        // Strategy 2: Find incorrect cells and suggest correct value
        for (let row = 0; row < gameState.size; row++) {
            for (let col = 0; col < gameState.size; col++) {
                if (userGrid[row][col] !== gameState.solution[row][col]) {
                    const correctValue = gameState.solution[row][col];
                    const userValue = userGrid[row][col];
                    setCurrentHint(`Cell (${row + 1}, ${col + 1}) is ${userValue} but should be ${correctValue}`);
                    setFocusedCell({ row, col });
                    setSelectedCell({ row, col });
                    return;
                }
            }
        }

        setCurrentHint('All cells are correct! Click "Check Solution" to verify.');
    };

    // Get cage for cell
    const getCageForCell = (row, col) => {
        if (!gameState) return null;
        return gameState.cages.find(cage =>
            cage.cells.some(([r, c]) => r === row && c === col)
        );
    };

    // Check if cell is cage start
    const isCageStart = (row, col) => {
        const cage = getCageForCell(row, col);
        if (!cage) return false;
        return cage.cells[0][0] === row && cage.cells[0][1] === col;
    };

    // Get cage border styles for visual grouping
    const getCageBorders = (row, col) => {
        const cage = getCageForCell(row, col);
        if (!cage) return {};

        const borders = {
            borderTopWidth: '3px',
            borderRightWidth: '3px',
            borderBottomWidth: '3px',
            borderLeftWidth: '3px',
        };

        // Check adjacent cells and make internal borders thinner
        const isInSameCage = (r, c) => {
            if (r < 0 || r >= gameState.size || c < 0 || c >= gameState.size) return false;
            const adjacentCage = getCageForCell(r, c);
            return adjacentCage && adjacentCage.id === cage.id;
        };

        // Thin internal borders, thick external borders
        if (isInSameCage(row - 1, col)) borders.borderTopWidth = '1px';
        if (isInSameCage(row + 1, col)) borders.borderBottomWidth = '1px';
        if (isInSameCage(row, col - 1)) borders.borderLeftWidth = '1px';
        if (isInSameCage(row, col + 1)) borders.borderRightWidth = '1px';

        // Use white and light gray for grouping visibility (always light, even in dark mode)
        const isLightGrayCage = cage.id % 2 === 0;
        borders.backgroundColor = isLightGrayCage ? '#f5f5f5' : '#ffffff';

        return borders;
    };

    if (!gameState) return <div>Loading...</div>;

    return (
        <div className="kenken-overlay" onClick={onClose}>
            <motion.div
                className="kenken-modal"
                onClick={(e) => e.stopPropagation()}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
            >
                {/* Header */}
                <div className="kenken-header">
                    <div className="kenken-title">
                        <Trophy size={24} />
                        <h2>KenKen Daily Challenge - {pillarName}</h2>
                    </div>
                    <button className="kenken-close" onClick={onClose}>
                        <X size={24} />
                    </button>
                </div>

                {/* Stats */}
                <div className="kenken-stats">
                    <div className="kenken-stat">
                        <Calendar size={20} />
                        <span>Today's Puzzle</span>
                    </div>
                    <div className="kenken-stat kenken-stat--streak">
                        <Flame size={20} />
                        <span>{streak} Day Streak</span>
                    </div>
                    <button
                        className="kenken-hint-btn"
                        onClick={() => setShowHints(!showHints)}
                    >
                        <HelpCircle size={20} />
                        <span>Rules</span>
                    </button>
                </div>

                {/* Rules */}
                <AnimatePresence>
                    {showHints && (
                        <motion.div
                            className="kenken-rules"
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                        >
                            <h3>📚 How to Play:</h3>
                            <ul>
                                <li><strong>Numbers:</strong> Fill each row and column with 1-{gameState.size} (no repeats)</li>
                                <li><strong>Cages:</strong> Each outlined group must equal its target using the operation</li>
                                <li><strong>Operations:</strong> + (add), - (subtract), × (multiply), ÷ (divide)</li>
                                <li><strong>Single cells:</strong> Just put that number in the cell</li>
                            </ul>
                            <h3>💡 Tips:</h3>
                            <ul>
                                <li>Start with single-cell cages (easiest to fill)</li>
                                <li>Use keyboard: Type numbers 1-{gameState.size}, arrow keys to move, Backspace to clear</li>
                                <li>Click any cell to select it, then type or use number pad</li>
                                <li>Look for the cage labels to identify which cells belong together</li>
                            </ul>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Game Grid */}
                <div className="kenken-grid-container">
                    <div
                        className="kenken-grid"
                        style={{
                            gridTemplateColumns: `repeat(${gameState.size}, 1fr)`,
                            gridTemplateRows: `repeat(${gameState.size}, 1fr)`
                        }}
                    >
                        {Array(gameState.size).fill(null).map((_, row) =>
                            Array(gameState.size).fill(null).map((_, col) => {
                                const cage = getCageForCell(row, col);
                                const isStart = isCageStart(row, col);
                                const cageBorders = getCageBorders(row, col);

                                return (
                                    <div
                                        key={`${row}-${col}`}
                                        className={`kenken-cell ${selectedCell?.row === row && selectedCell?.col === col ? 'kenken-cell--selected' : ''}`}
                                        style={cageBorders}
                                        onClick={() => {
                                            setSelectedCell({ row, col });
                                            setFocusedCell({ row, col });
                                        }}
                                    >
                                        {isStart && cage && (
                                            <div className="kenken-cage-label">
                                                {cage.target}{cage.operation || ''}
                                            </div>
                                        )}
                                        <input
                                            type="text"
                                            inputMode="numeric"
                                            pattern={`[1-${gameState.size}]`}
                                            maxLength="1"
                                            value={userGrid[row][col] || ''}
                                            onChange={(e) => handleCellInput(row, col, e.target.value)}
                                            onKeyPress={(e) => {
                                                // Only allow numbers 1 to size
                                                const char = e.key;
                                                if (!/[0-9]/.test(char)) {
                                                    e.preventDefault();
                                                } else {
                                                    const num = parseInt(char);
                                                    if (num < 1 || num > gameState.size) {
                                                        e.preventDefault();
                                                    }
                                                }
                                            }}
                                            className="kenken-input"
                                            disabled={isComplete}
                                        />
                                    </div>
                                );
                            })
                        )}
                    </div>
                </div>

                {/* Number Pad */}
                {!isComplete && (
                    <div className="kenken-numpad">
                        {Array(gameState.size).fill(null).map((_, num) => (
                            <button
                                key={num + 1}
                                className="kenken-num-btn"
                                onClick={() => {
                                    if (selectedCell) {
                                        handleCellInput(selectedCell.row, selectedCell.col, num + 1);
                                    }
                                }}
                            >
                                {num + 1}
                            </button>
                        ))}
                        <button
                            className="kenken-num-btn kenken-num-btn--clear"
                            onClick={() => {
                                if (selectedCell) {
                                    handleCellInput(selectedCell.row, selectedCell.col, 0);
                                }
                            }}
                        >
                            Clear
                        </button>
                        <button
                            className="kenken-num-btn kenken-num-btn--hint"
                            onClick={generateHint}
                            disabled={isComplete}
                        >
                            💡 Hint
                        </button>
                    </div>
                )}

                {/* Current Hint Display */}
                {currentHint && !isComplete && (
                    <motion.div
                        className="kenken-hint-display"
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                    >
                        <HelpCircle size={18} />
                        <span>{currentHint}</span>
                        <button
                            className="kenken-hint-close"
                            onClick={() => setCurrentHint(null)}
                        >
                            <X size={16} />
                        </button>
                    </motion.div>
                )}

                {/* Errors */}
                {errors.length > 0 && (
                    <div className="kenken-errors">
                        {errors.slice(0, 3).map((error, idx) => (
                            <div key={idx} className="kenken-error">{error}</div>
                        ))}
                    </div>
                )}

                {/* Success Message */}
                <AnimatePresence>
                    {isComplete && (
                        <motion.div
                            className="kenken-success"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: 20 }}
                        >
                            <Trophy size={48} />
                            <h3>Puzzle Complete! 🎉</h3>
                            <p>Your streak: {streak} days</p>
                            <p>Come back tomorrow for a new challenge!</p>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Actions */}
                <div className="kenken-actions">
                    <button className="kenken-btn kenken-btn--secondary" onClick={resetPuzzle}>
                        <RefreshCw size={18} />
                        Reset
                    </button>
                    <button
                        className="kenken-btn kenken-btn--primary"
                        onClick={checkSolution}
                        disabled={isComplete}
                    >
                        <Check size={18} />
                        Check Solution
                    </button>
                </div>
            </motion.div>
        </div>
    );
};

export default KenKenGame;
