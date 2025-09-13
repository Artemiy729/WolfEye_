import type { ReactNode } from "react";

// Определяем интерфейс для свойств компонента Container
interface ContainerProps {
    // Дочерние элементы, которые будут отображаться внутри контейнера
    children: ReactNode
    // Дополнительный класс для стилизации
    className?: string
    // Размер контейнера: маленький, средний, большой, очень большой или полный
    size?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
}

// Функциональный компонент Container
export function Container({ children, className = '', size = 'xl' }: ContainerProps) {
    // Определяем максимальную ширину для каждого размера контейнера
    const sizes = {
        sm: 'max-w-2xl', // Маленький размер
        md: 'max-w-4xl', // Средний размер
        lg: 'max-w-6xl', // Большой размер
        xl: 'max-w-7xl', // Очень большой размер
        full: 'max-w-full' // Полный размер
    }
    
    return (
        // Возвращаем TSX с применением стилей и дополнительных классов
        <div className={`mx-auto px-4 sm:px-6 lg:px-8 ${sizes[size]} ${className}`}>
            {children}
        </div>
    )
}