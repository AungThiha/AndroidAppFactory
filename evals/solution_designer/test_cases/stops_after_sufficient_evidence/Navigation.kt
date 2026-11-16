package fixture

import androidx.lifecycle.LifecycleCoroutineScope
import androidx.navigation.NavHostController
import androidx.navigation.NavOptionsBuilder
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Deferred
import kotlinx.coroutines.Job
import kotlinx.coroutines.async
import kotlinx.coroutines.launch

interface Destination {
    val route: String
}

sealed class BackStackOptions {
    data object Clear : BackStackOptions()
    data class PopUpTo(val destination: Destination, val inclusive: Boolean = false) : BackStackOptions()
}

data class NavigationOptions(
    val launchSingleTop: Boolean = false,
    val backStackOptions: BackStackOptions? = null,
)

interface NavigationHandler {
    fun onNavigateUp(): Deferred<Boolean>
    fun onNavigation(destination: Destination, options: NavigationOptions): Job
}

fun NavigationHandler(
    lifecycleScope: LifecycleCoroutineScope,
    navHostController: NavHostController,
) = object : NavigationHandler {
    override fun onNavigateUp() = lifecycleScope.async(AppDispatchers.main) {
        navHostController.navigateUp()
    }

    override fun onNavigation(destination: Destination, options: NavigationOptions) =
        lifecycleScope.launch(AppDispatchers.main) {
            navHostController.navigateTo(destination, options)
        }
}

fun NavHostController.navigateTo(destination: Destination, options: NavigationOptions) {
    navigate(destination.route) {
        applyNavigationOptions(options)
    }
}

fun NavOptionsBuilder.applyNavigationOptions(options: NavigationOptions) {
    launchSingleTop = options.launchSingleTop
    when (val backStack = options.backStackOptions) {
        null -> Unit
        BackStackOptions.Clear -> popUpTo(0)
        is BackStackOptions.PopUpTo -> popUpTo(backStack.destination.route) {
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

    fun navigate(
        destination: Destination,
        launchSingleTop: Boolean = false,
        clearBackStack: Boolean = false,
    ): Job = navigate(
        destination,
        NavigationOptions(launchSingleTop, if (clearBackStack) BackStackOptions.Clear else null),
    )

    fun navigate(destination: Destination, popUpTo: Destination, inclusive: Boolean = false): Job =
        navigate(destination, NavigationOptions(backStackOptions = BackStackOptions.PopUpTo(popUpTo, inclusive)))
}

object AppDispatchers {
    var testMain: CoroutineDispatcher? = null
    val main: CoroutineDispatcher get() = testMain ?: Dispatchers.Main
}
