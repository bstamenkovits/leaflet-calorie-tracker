import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { FoodLogComponent } from './pages/food-log/food-log.component';
import { WeightLogComponent } from './pages/weight-log/weight-log.component';
import { AgentComponent } from './pages/agent/agent.component';
import { RecipesComponent } from './pages/recipes/recipes.component';
import { ProfileComponent } from './pages/profile/profile.component';

export const routes: Routes = [
  { path: '', redirectTo: '/food-log', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'food-log', component: FoodLogComponent },
  { path: 'weight-log', component: WeightLogComponent },
  { path: 'agent', component: AgentComponent },
  { path: 'recipes', component: RecipesComponent },
  { path: 'profile', component: ProfileComponent }
];
