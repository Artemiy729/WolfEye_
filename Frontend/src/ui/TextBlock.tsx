// Определяем интерфейс для свойств компонента TextBlock
interface TextBlockProps {
    // Заголовок блока текста
    title: string;
    // Подзаголовок блока текста (необязательный)
    subtitle?: string;
    // Основное содержимое блока текста (необязательное)
    content?: string;
}

// Функциональный компонент TextBlock
export function TextBlock({ title, subtitle, content }: TextBlockProps) {
    return (
        <div className="text-white">
            {/* Отображаем заголовок с различными размерами шрифта в зависимости от экрана */}
            <h1 className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-extrabold tracking-tight leading-[1.1]">{title}</h1>
            {/* Если подзаголовок передан, отображаем его */}
            {subtitle && <h2 className="mt-3 text-3xl text-white">{subtitle}</h2>}
            {/* Если содержимое передано, отображаем его */}
            {content && <p className="mt-6 text-lg text-white">{content}</p>}
        </div>
    )
}