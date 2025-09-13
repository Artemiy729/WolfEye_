interface LogoProps {
    className?: string
    size?: 'sm' | 'md' | 'lg' | 'xl'
    showText?: boolean
  }
  
  export function Logo({ className = '', size = 'md', showText = true }: LogoProps) {
    const iconSizes: Record<NonNullable<LogoProps['size']>, string> = {
      sm: 'w-12 h-12',
      md: 'w-24 h-24',
      lg: 'w-32 h-32',
      xl: 'w-48 h-48',
    }
    
    return (
      <div className={`flex items-center ${showText ? 'space-x-3' : ''} ${className}`}>
        <img src="/wolfeye.svg?v=1" alt="Глаз Волка" className={`${iconSizes[size]}`} />
        {showText && <span className="text-xl font-bold text-white">ГЛАЗ ВОЛКА</span>}
      </div>
    )
  }