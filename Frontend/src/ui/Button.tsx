import { forwardRef } from "react";
import type { ReactNode, ButtonHTMLAttributes } from "react";

// Определяем интерфейс для свойств компонента Button, расширяющий стандартные атрибуты HTMLButtonElement
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  // Вариант отображения кнопки: основной, второстепенный или "призрачный"
  variant?: "primary" | "secondary" | "ghost";
  // Размер кнопки: маленький, средний или большой
  size?: "sm" | "md" | "lg";
  // Дочерние элементы, которые будут отображаться внутри кнопки
  children: ReactNode;
}

// Базовые стили для кнопки, применяемые ко всем вариантам
const baseStyles =
  "inline-flex items-center justify-center rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none";

// Стили для каждого варианта кнопки
const variants = {
  primary: "bg-cyan-500 hover:bg-cyan-600 text-white focus:ring-cyan-500", // Основной стиль
  secondary: "bg-gray-700 hover:bg-gray-600 text-white focus:ring-gray-500", // Второстепенный стиль
  ghost: "text-white hover:bg-gray-800 focus:ring-gray-500", // "Призрачный" стиль
} satisfies Record<NonNullable<ButtonProps["variant"]>, string>;

// Стили для каждого размера кнопки
const sizes = {
  sm: "px-3 py-2 text-sm", // Маленький размер
  md: "px-6 py-3 text-base", // Средний размер
  lg: "px-8 py-4 text-lg", // Большой размер
} satisfies Record<NonNullable<ButtonProps["size"]>, string>;

// Функция для объединения классов в одну строку
function joinClasses(a: string, b?: string, c?: string, d?: string): string {
  return [a, b, c, d].filter(Boolean).join(" ");
}

// Экспортируемый компонент Button с поддержкой передачи ссылки (ref)
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(function Button(
  { variant = "primary", size = "md", type = "button", className, children, ...props },
  ref
) {
  // Объединяем все стили в одну строку
  const classNames = joinClasses(baseStyles, variants[variant], sizes[size], className);
  return (
    // Возвращаем TSX для кнопки с применением всех стилей и переданных свойств
    <button ref={ref} type={type} className={classNames} {...props}>
      {children}
    </button>
  );
});