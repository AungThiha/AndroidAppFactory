package fixture

import androidx.lifecycle.LifecycleCoroutineScope
import androidx.navigation.NavHostController
import androidx.navigation.NavOptionsBuilder
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch

interface Destination

sealed class BackStackOptions {
    data object Clear : BackStackOptions()
    data class PopUpTo(val destination: Destination, val inclusive: Boolean = false) : BackStackOptions()
}

data class NavigationOptions(
    val launchSingleTop: Boolean = false,
    val backStackOptions: BackStackOptions? = null,
)

interface NavigationHandler {
    fun onNavigation(destination: Destination, options: NavigationOptions): Job
}

fun NavigationHandler(
    lifecycleScope: LifecycleCoroutineScope,
    navHostController: NavHostController,
) = object : NavigationHandler {
    override fun onNavigation(destination: Destination, options: NavigationOptions) =
        lifecycleScope.launch(AppDispatchers.main) {
            navHostController.navigate(destination) {
                applyNavigationOptions(options)
            }
        }
}

fun NavOptionsBuilder.applyNavigationOptions(options: NavigationOptions) {
    launchSingleTop = options.launchSingleTop
    when (val backStack = options.backStackOptions) {
        null -> Unit
        BackStackOptions.Clear -> popUpTo(0)
        is BackStackOptions.PopUpTo -> popUpTo(backStack.destination) {
            inclusive = backStack.inclusive
        }
    }
}

class NavigationDispatcher {
    private lateinit var handler: NavigationHandler

    fun setHandler(handler: NavigationHandler) {
        this.handler = handler
    }

    fun navigate(destination: Destination, options: NavigationOptions): Job =
        handler.onNavigation(destination, options)
}

object AppDispatchers {
    var testMain: CoroutineDispatcher? = null
    val main: CoroutineDispatcher get() = testMain ?: Dispatchers.Main
}
