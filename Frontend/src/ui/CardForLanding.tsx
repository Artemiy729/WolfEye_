import type { ReactNode } from "react";

// Определяем интерфейс для свойств компонента Card
interface CardProps {
    // Дочерние элементы, которые будут отображаться внутри карточки
    children: ReactNode
    // Дополнительный класс для стилизации
    className?: string
    // Вариант отображения карточки: по умолчанию, с обводкой или с тенью
    variant?: 'default' | 'outlined' | 'elevated'
}

// Функциональный компонент Card
export function Card({ children, className = '', variant = 'default' }: CardProps) {
    // Определяем стили для каждого варианта отображения
    const variants = {
        default: 'bg-[#0e1a30] border border-gray-700', // Стиль по умолчанию
        outlined: 'border border-gray-600 bg-transparent', // Стиль с обводкой
        elevated: 'bg-[#0e1a30] shadow-xl border border-gray-700' // Стиль с тенью
    }
    
    return (
        // Возвращаем TSX с применением стилей, анимации и дополнительных классов
        // transition-transform - плавный переход для трансформации
        // duration-200 - длительность анимации 200мс
        // ease-out - замедление к концу анимации для естественности
        // transform-gpu - использует GPU для плавности анимации
        // hover:scale-[1.02] - увеличение на 2% при наведении мыши
        <div className={`rounded-lg p-6 transition-transform duration-200 ease-out transform-gpu hover:scale-[1.05] ${variants[variant]} ${className}`}>
            {children} 
        </div>
    )
}