interface LogoProps {
    className?: string
    size?: 'sm' | 'md' | 'lg'
  }
  
  export function Logo({ className = '', size = 'md' }: LogoProps) {
    const sizes = {
      sm: 'w-8 h-8',
      md: 'w-12 h-12',
      lg: 'w-16 h-16'
    }
    
    return (
      <div className={`flex items-center space-x-3 ${className}`}>
        <div className={`${sizes[size]} rounded-full border-2 border-cyan-400 flex items-center justify-center`}>
          <svg 
            className="w-6 h-6 text-cyan-400" 
            fill="currentColor" 
            viewBox="0 0 24 24"
          >
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
          </svg>
        </div>
        <span className="text-xl font-bold text-white">ГЛАЗ ВОЛКА</span>
      </div>
    )
  }