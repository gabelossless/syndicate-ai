import React from 'react';
import { Wallet, Menu } from 'lucide-react';

const Header = () => {
    const [address, setAddress] = React.useState(null);

    const connectWallet = () => {
        const mockAddress = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e";
        setAddress(mockAddress);
    };

    return (
        <header className="sticky top-0 z-50 w-full bg-brand-bg/60 border-b border-brand-border backdrop-blur-md">
            <div className="container mx-auto px-6 py-4 flex justify-between items-center">
                <div className="flex items-center gap-4 group cursor-pointer">
                    <div className="w-10 h-10 bg-brand-primary/20 border border-brand-primary/40 rounded-xl flex items-center justify-center group-hover:shadow-[0_0_15px_rgba(16,185,129,0.3)] transition-all">
                        <span className="font-black text-brand-primary tracking-tighter text-lg leading-none">S.ai</span>
                    </div>
                    <h1 className="text-xl font-bold tracking-tight text-white/90">
                        Syndicate<span className="text-brand-primary">.ai</span>
                    </h1>
                </div>

                <div className="flex gap-6 items-center">
                    <nav className="hidden md:flex gap-8 text-xs font-black uppercase tracking-widest text-white/40">
                        <a href="#" className="hover:text-brand-primary transition-colors">Markets</a>
                        <a href="#" className="hover:text-brand-primary transition-colors">Signals</a>
                        <a href="#" className="hover:text-brand-primary transition-colors">API docs</a>
                    </nav>

                    {address ? (
                        <div className="font-mono bg-brand-primary/10 px-4 py-2 border border-brand-primary/30 rounded-xl text-xs text-brand-primary font-bold">
                            {address.slice(0, 6)}...{address.slice(-4)}
                        </div>
                    ) : (
                        <button
                            onClick={connectWallet}
                            className="bg-brand-primary text-black px-5 py-2 rounded-xl font-bold text-sm hover:scale-105 active:scale-95 transition-all shadow-[0_4px_20px_rgba(16,185,129,0.2)]"
                        >
                            CONNECT
                        </button>
                    )}

                    <button className="md:hidden text-white/60">
                        <Menu size={24} />
                    </button>
                </div>
            </div>
        </header>
    );
};

export default Header;
