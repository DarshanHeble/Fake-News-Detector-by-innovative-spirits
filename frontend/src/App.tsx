// src/App.tsx
import React from 'react';
import FakeNewsChecker from './Components/FakeNewsChecker';

const App: React.FC = () => {
    return (
        <div className="App">
            <FakeNewsChecker />
        </div>
    );
};

export default App;