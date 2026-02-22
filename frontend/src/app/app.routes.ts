import { Routes } from '@angular/router';
import { OverviewComponent } from './pages/overview/agent.component';
import { LogComponent } from './pages/log/log.component';
import { AgentComponent } from './pages/agent/agent.component';
import { RecipesComponent } from './pages/recipes/recipes.component';
import { ProfileComponent } from './pages/profile/profile.component';

export const routes: Routes = [
  { path: '', redirectTo: '/overview', pathMatch: 'full' },
  { path: 'overview', component: OverviewComponent },
  { path: 'agent', component: AgentComponent },
  { path: 'log', component: LogComponent },
  { path: 'recipes', component: RecipesComponent },
  { path: 'profile', component: ProfileComponent }
];
