interface TextBlockProps {
    title: string;
    subtitle?: string;
    content?: string;
}

export function TextBlock({ title, subtitle, content }: TextBlockProps) {
    return (
        <div className="text-white">
            <h1 className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-extrabold tracking-tight leading-[1.1]">{title}</h1>
            {subtitle && <h2 className="mt-3 text-3xl text-white">{subtitle}</h2>}
            {content && <p className="mt-6 text-lg text-white">{content}</p>}
        </div>
    )
}