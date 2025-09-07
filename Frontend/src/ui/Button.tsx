import type { ReactNode, ButtonHTMLAttributes } from "react";

// Интерфейс для свойств кнопки
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'ghost' // Варианты стилей кнопки
    size?: 'sm' | 'md' | 'lg' // Размеры кнопки
    children: ReactNode // Дочерние элементы, которые будут внутри кнопки
}

// Функциональный компонент Button
export function Button({
    variant = 'primary', // Значение по умолчанию для варианта стиля
    size = 'md', // Значение по умолчанию для размера
    className = '', // Дополнительные классы CSS
    children, // Дочерние элементы
    ...props // Остальные свойства, переданные в компонент
}: ButtonProps) {
    // Базовые стили для кнопки
    const baseStyles = 'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none'
    
    // Стили для каждого варианта кнопки
    const variants = {
        primary: 'bg-cyan-500 hover:bg-cyan-600 text-white focus:ring-cyan-500',
        secondary: 'bg-gray-700 hover:bg-gray-600 text-white focus:ring-gray-500',
        ghost: 'text-white hover:bg-gray-800 focus:ring-gray-500'
    }

    // Стили для каждого размера кнопки
    const sizes = {
        sm: 'px-3 py-2 text-sm',
        md: 'px-6 py-3 text-base',
        lg: 'px-8 py-4 text-lg'
    }

    // Возвращаем JSX для кнопки
    return (
        <button
            className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`} // Объединяем все стили
            {...props} // Применяем остальные свойства
        >
            {children}
        </button>
    )
}