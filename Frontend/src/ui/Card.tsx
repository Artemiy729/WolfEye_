import type { ReactNode } from "react";

interface CardProps {
    children: ReactNode
    className?: string
    variant?: 'default' | 'outlined' | 'elevated'
  }

  export function Card({ children, className = '', variant = 'default' }: CardProps) {
    const variants = {
      default: 'bg-gray-800 border border-gray-700',
      outlined: 'border border-gray-600 bg-transparent',
      elevated: 'bg-gray-800 shadow-xl border border-gray-700'
    }
    
    return (
      <div className={`rounded-lg p-6 ${variants[variant]} ${className}`}>
        {children}
      </div>
    )
  }