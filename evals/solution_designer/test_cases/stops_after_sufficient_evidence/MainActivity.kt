package fixture

import androidx.activity.ComponentActivity
import androidx.lifecycle.lifecycleScope
import androidx.navigation.NavHostController

class MainActivity : ComponentActivity() {
    fun installNavigation(
        navigationDispatcher: NavigationDispatcher,
        navHostController: NavHostController,
    ) {
        navigationDispatcher.setHandler(
            NavigationHandler(lifecycleScope, navHostController)
        )
    }
}
