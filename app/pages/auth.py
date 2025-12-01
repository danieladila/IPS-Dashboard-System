import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="absolute inset-0 bg-pattern-grid opacity-10 pointer-events-none"
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "file-check-2",
                        class_name="h-24 w-24 stroke-white opacity-20 stroke-1",
                    ),
                    class_name="transform -rotate-12 hover:scale-110 transition-transform duration-700 ease-in-out",
                ),
                rx.el.div(
                    rx.icon(
                        "briefcase",
                        class_name="h-20 w-20 stroke-blue-200 opacity-20 stroke-1",
                    ),
                    class_name="mr-12 mt-16 transform rotate-6 hover:scale-110 transition-transform duration-700 ease-in-out",
                ),
                rx.el.div(
                    rx.icon(
                        "shield-check",
                        class_name="h-16 w-16 stroke-indigo-200 opacity-20 stroke-1",
                    ),
                    class_name="ml-8 mt-12 transform -rotate-6 hover:scale-110 transition-transform duration-700 ease-in-out",
                ),
                class_name="hidden lg:flex flex-1 flex-col justify-center items-end pr-16 h-full select-none pointer-events-none",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Industrial Project Service",
                        class_name="mx-auto text-center text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white to-blue-200 drop-shadow-lg tracking-tight mb-2",
                    ),
                    rx.el.h2(
                        "Dashboard System",
                        class_name="mt-2 text-center text-xl font-medium text-blue-100 drop-shadow-md",
                    ),
                    class_name="sm:mx-auto sm:w-full sm:max-w-md relative z-10",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.form(
                            rx.el.div(
                                rx.el.label(
                                    "Email address",
                                    html_for="email",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.div(
                                    rx.el.input(
                                        type="email",
                                        name="email",
                                        required=True,
                                        placeholder="you@example.com",
                                        class_name="appearance-none block w-full px-4 py-3 border border-gray-300 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all",
                                    ),
                                    class_name="mt-1",
                                ),
                                class_name="mb-5",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Password",
                                    html_for="password",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.div(
                                    rx.el.input(
                                        type="password",
                                        name="password",
                                        required=True,
                                        placeholder="********",
                                        class_name="appearance-none block w-full px-4 py-3 border border-gray-300 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all",
                                    ),
                                    class_name="mt-1",
                                ),
                                class_name="mb-8",
                            ),
                            rx.cond(
                                AuthState.error_message != "",
                                rx.el.div(
                                    rx.icon(
                                        "badge_alert",
                                        class_name="h-4 w-4 text-red-500 mr-2",
                                    ),
                                    AuthState.error_message,
                                    class_name="mb-6 p-3 text-sm text-red-700 bg-red-50 border border-red-100 rounded-xl flex items-center",
                                ),
                            ),
                            rx.el.button(
                                "Sign in",
                                type="submit",
                                class_name="w-full flex justify-center py-3 px-4 border border-transparent rounded-xl shadow-lg text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all transform hover:-translate-y-0.5",
                            ),
                            rx.el.div(
                                "Don't have an account? ",
                                rx.el.a(
                                    "Create a new account",
                                    href="/register",
                                    class_name="font-medium text-blue-600 hover:text-blue-500 transition-colors",
                                ),
                                class_name="mt-6 text-center text-sm text-gray-600",
                            ),
                            on_submit=AuthState.login,
                        ),
                        class_name="glass-card py-8 px-4 shadow-2xl sm:rounded-2xl sm:px-10 relative z-10",
                    ),
                    class_name="mt-8 sm:mx-auto sm:w-full sm:max-w-md",
                ),
                class_name="w-full max-w-md flex flex-col justify-center z-20 mx-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "bar-chart-3",
                        class_name="h-24 w-24 stroke-white opacity-20 stroke-1",
                    ),
                    class_name="transform rotate-12 hover:scale-110 transition-transform duration-700 ease-in-out",
                ),
                rx.el.div(
                    rx.icon(
                        "lightbulb",
                        class_name="h-20 w-20 stroke-purple-200 opacity-20 stroke-1",
                    ),
                    class_name="ml-12 mt-16 transform -rotate-6 hover:scale-110 transition-transform duration-700 ease-in-out",
                ),
                rx.el.div(
                    rx.icon(
                        "users",
                        class_name="h-16 w-16 stroke-blue-200 opacity-20 stroke-1",
                    ),
                    class_name="mr-8 mt-12 transform rotate-6 hover:scale-110 transition-transform duration-700 ease-in-out",
                ),
                class_name="hidden lg:flex flex-1 flex-col justify-center items-start pl-16 h-full select-none pointer-events-none",
            ),
            class_name="flex flex-row items-center justify-center w-full max-w-7xl mx-auto h-full relative",
        ),
        class_name="min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8 bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 animate-gradient-xy relative overflow-hidden",
    )


def register_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="absolute inset-0 bg-pattern-grid opacity-10 pointer-events-none"
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Industrial Project Service",
                    class_name="mx-auto text-center text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white to-blue-200 drop-shadow-lg tracking-tight mb-2",
                ),
                rx.el.h2(
                    "Dashboard System",
                    class_name="mt-2 text-center text-xl font-medium text-blue-100 drop-shadow-md",
                ),
                rx.el.p(
                    "Or ",
                    rx.el.a(
                        "sign in to existing account",
                        href="/login",
                        class_name="font-medium text-blue-100 hover:text-white transition-colors underline decoration-blue-300/50 hover:decoration-white",
                    ),
                    class_name="mt-2 text-center text-sm text-blue-100",
                ),
                class_name="sm:mx-auto sm:w-full sm:max-w-md relative z-10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.form(
                        rx.el.div(
                            rx.el.label(
                                "Username",
                                html_for="username",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.div(
                                rx.el.input(
                                    type="text",
                                    name="username",
                                    required=True,
                                    class_name="appearance-none block w-full px-4 py-2.5 border border-gray-300 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all",
                                ),
                                class_name="mt-1",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Email address",
                                html_for="email",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.div(
                                rx.el.input(
                                    type="email",
                                    name="email",
                                    required=True,
                                    class_name="appearance-none block w-full px-4 py-2.5 border border-gray-300 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all",
                                ),
                                class_name="mt-1",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Password",
                                html_for="password",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.div(
                                rx.el.input(
                                    type="password",
                                    name="password",
                                    required=True,
                                    class_name="appearance-none block w-full px-4 py-2.5 border border-gray-300 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all",
                                ),
                                class_name="mt-1",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Confirm Password",
                                html_for="confirm_password",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.div(
                                rx.el.input(
                                    type="password",
                                    name="confirm_password",
                                    required=True,
                                    class_name="appearance-none block w-full px-4 py-2.5 border border-gray-300 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all",
                                ),
                                class_name="mt-1",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Role",
                                html_for="role",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option("Employee", value="Employee"),
                                    rx.el.option("Manager", value="Manager"),
                                    rx.el.option("Admin", value="Admin"),
                                    name="role",
                                    class_name="block w-full px-4 py-2.5 border border-gray-300 bg-white rounded-xl shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all",
                                ),
                                class_name="mt-1",
                            ),
                            class_name="mb-6",
                        ),
                        rx.cond(
                            AuthState.error_message != "",
                            rx.el.div(
                                rx.icon(
                                    "badge_alert",
                                    class_name="h-4 w-4 text-red-500 mr-2",
                                ),
                                AuthState.error_message,
                                class_name="mb-6 p-3 text-sm text-red-700 bg-red-50 border border-red-100 rounded-xl flex items-center",
                            ),
                        ),
                        rx.el.button(
                            "Create Account",
                            type="submit",
                            class_name="w-full flex justify-center py-3 px-4 border border-transparent rounded-xl shadow-lg text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all transform hover:-translate-y-0.5",
                        ),
                        on_submit=AuthState.register,
                    ),
                    class_name="glass-card py-8 px-4 shadow-2xl sm:rounded-2xl sm:px-10 relative z-10",
                ),
                class_name="mt-8 sm:mx-auto sm:w-full sm:max-w-md",
            ),
            class_name="min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8 bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 animate-gradient-xy relative overflow-hidden",
        ),
    )