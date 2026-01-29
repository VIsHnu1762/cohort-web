import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Gamepad2, Trophy, Puzzle, Brain } from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import KenKenGame from '../../components/games/KenKenGame';
import './Games.css';

export const Games = () => {
    const [selectedGame, setSelectedGame] = useState(null);

    const games = [
        {
            id: 'kenken',
            name: 'KenKen Puzzle',
            description: 'Daily mathematical logic puzzle. Solve a new 4x4 KenKen puzzle each day and maintain your streak!',
            icon: Brain,
            color: 'linear-gradient(135deg, #ffcc00 0%, #FFA726 100%)',
            borderColor: 'rgba(247, 201, 72, 0.5)',
        },
        // More games can be added here in the future
    ];

    return (
        <div className="games-container">
            {/* Header */}
            <motion.div
                className="games-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
            >
                <div className="games-header-content">
                    <div className="games-icon-wrapper">
                        <Gamepad2 size={48} />
                    </div>
                    <div>
                        <h1 className="games-title">Brain Games</h1>
                        <p className="games-subtitle">
                            Challenge yourself with daily puzzles and track your progress
                        </p>
                    </div>
                </div>
            </motion.div>

            {/* Games Grid */}
            <div className="games-grid">
                {games.map((game, index) => {
                    const GameIcon = game.icon;
                    return (
                        <motion.div
                            key={game.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1, duration: 0.5 }}
                        >
                            <GlassCard variant="heavy" className="game-card">
                                <div className="game-card-content">
                                    <div
                                        className="game-icon"
                                        style={{
                                            background: game.color,
                                            border: `2px solid ${game.borderColor}`
                                        }}
                                    >
                                        <GameIcon size={32} />
                                    </div>

                                    <h3 className="game-name">{game.name}</h3>
                                    <p className="game-description">{game.description}</p>

                                    <button
                                        className="play-button"
                                        type="button"
                                        onClick={() => {
                                            console.log('Button clicked, setting game:', game.id);
                                            setSelectedGame(game.id);
                                        }}
                                    >
                                        <Trophy size={20} />
                                        Play Daily Challenge
                                    </button>
                                </div>
                            </GlassCard>
                        </motion.div>
                    );
                })}
            </div>

            {/* Coming Soon Section */}
            <motion.div
                className="coming-soon-section"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3, duration: 0.6 }}
            >
                <GlassCard variant="light" className="coming-soon-card">
                    <Puzzle size={32} className="coming-soon-icon" />
                    <h3 className="coming-soon-title">More Games Coming Soon!</h3>
                    <p className="coming-soon-text">
                        Stay tuned for more exciting brain games and challenges to test your skills.
                    </p>
                </GlassCard>
            </motion.div>

            {/* Game Modals */}
            <AnimatePresence>
                {selectedGame === 'kenken' && (
                    <KenKenGame
                        onClose={() => setSelectedGame(null)}
                        pillarName="Games"
                    />
                )}
            </AnimatePresence>
        </div>
    );
};

export default Games;
