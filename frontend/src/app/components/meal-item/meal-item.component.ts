import { Component, Input, OnInit } from '@angular/core';
import { MealItem } from '../../services/mock-data.service';

@Component({
  selector: 'meal-item',
  standalone: true,
  imports: [],
  templateUrl: './meal-item.component.html',
  styleUrls: ['./meal-item.component.css']
})
export class MealItemComponent implements OnInit {
  @Input({ required: true }) item!: MealItem;
  @Input() expanded = false;
  isExpanded = false;

  ngOnInit() {
    this.isExpanded = this.expanded;
  }
}
