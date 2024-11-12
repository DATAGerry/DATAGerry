import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-report-overview',
  templateUrl: './report-overview.component.html',
  styleUrls: ['./report-overview.component.scss']
})
export class ReportOverviewComponent {
  constructor(private router: Router) { }

  // Method to navigate to the Report Category Overview component
  navigateToCategories(): void {
    this.router.navigate(['/report-categories']);
  }
}
