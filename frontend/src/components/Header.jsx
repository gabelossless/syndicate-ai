import React from 'react';
import { Wallet, Menu } from 'lucide-react';

const Header = () => {
    const [address, setAddress] = React.useState(null);

    const connectWallet = () => {
        // Simulate Web3 Connection
        const mockAddress = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e";
        setAddress(mockAddress);
    };

    return (
        <header className="flex justify-between items-center p-6 border-b-4 border-neo-black bg-neo-white sticky top-0 z-50">
            <div className="flex items-center gap-4">
                <div className="bg-neo-green w-12 h-12 border-2 border-neo-black flex items-center justify-center shadow-neo-sm">
                    <span className="font-mono font-bold text-xl">S.ai</span>
                </div>
                <h1 className="text-3xl tracking-tighter">Syndicate<span className="text-neo-pink">.ai</span></h1>
            </div>

            <div className="flex gap-4 items-center">
                {address ? (
                    <div className="font-mono bg-neo-green px-3 py-2 border-2 border-neo-black shadow-neo-sm text-sm">
                        {address.slice(0, 6)}...{address.slice(-4)}
                    </div>
                ) : (
                    <button
                        onClick={connectWallet}
                        className="neo-btn bg-neo-yellow hover:bg-neo-yellow/80 flex items-center gap-2"
                    >
                        <Wallet size={20} />
                        <span>Connect Wallet</span>
                    </button>
                )}
                <button className="p-3 border-2 border-neo-black shadow-neo-sm hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all">
                    <Menu size={24} />
                </button>
            </div>
        </header>
    );
};

export default Header;
