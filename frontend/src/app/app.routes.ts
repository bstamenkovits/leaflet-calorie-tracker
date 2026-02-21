import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { FoodLogComponent } from './pages/food-log/food-log.component';
import { ProfileComponent } from './pages/profile/profile.component';

export const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'food-log', component: FoodLogComponent },
  { path: 'profile', component: ProfileComponent }
];
