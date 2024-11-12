import { Component, OnInit, OnDestroy, TemplateRef, ViewChild } from '@angular/core';
import { Router } from '@angular/router';

import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ReportCategoryService } from 'src/app/reporting/services/report-category.service';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { APIGetMultiResponse } from 'src/app/services/models/api-response';
import { AddCategoryModalComponent } from '../category-add-modal/category-add-modal.component';

@Component({
    selector: 'app-category-overview',
    templateUrl: './category-overview.component.html',
    styleUrls: ['./category-overview.component.scss']
})
export class CategoryOverviewComponent implements OnInit, OnDestroy {
    private unsubscribe$ = new ReplaySubject<void>(1);
    public categories: Array<any> = [];
    public totalCategories: number = 0;
    public loading = false;

    @ViewChild('actionsTemplate', { static: true }) actionsTemplate: TemplateRef<any>;

    public columns: Array<any>;

    constructor(private categoryService: ReportCategoryService, private router: Router) { }

    ngOnInit(): void {
        this.columns = [
            { display: 'Public ID', name: 'public_id', data: 'public_id', sortable: true, style: { width: '120px', 'text-align': 'center' } },
            { display: 'Name', name: 'name', data: 'name', sortable: true, style: { width: 'auto', 'text-align': 'center' } },
            { display: 'Actions', name: 'actions', template: this.actionsTemplate, sortable: false, style: { width: '100px', 'text-align': 'center' } }
        ];

        this.postDummyData();

        this.loadCategories();
    }

    ngOnDestroy(): void {
        this.unsubscribe$.next();
        this.unsubscribe$.complete();
    }


    private postDummyData(): void {
        const dummyCategory = {
            name: 'Sample Category',
            predefined: false
        };

        this.categoryService.postDummyCategory().subscribe(
            (response) => {
                console.log('Dummy data posted successfully:', response);
            },
            (error) => {
                console.error('Error posting dummy data:', error);
            }
        );
    }

    private loadCategories(): void {
        this.loading = true;
        const params: CollectionParameters = {
            filter: {},
            limit: 10,
            sort: 'public_id',
            order: 1,
            page: 1
        };
        this.categoryService.getAllCategories(params).pipe(takeUntil(this.unsubscribe$)).subscribe(
            (response: APIGetMultiResponse<any>) => {
                this.categories = response.results;
                this.totalCategories = response.total;
                this.loading = false;

                console.log('categories', response.results)
            }
        );
    }

    public editCategory(id: number): void {
        console.log('Edit category with ID:', id);
    }

    public deleteCategory(id: number): void {
        if (confirm('Are you sure you want to delete this category?')) {
            this.categoryService.deleteCategory(id).pipe(takeUntil(this.unsubscribe$)).subscribe(
                () => {
                    alert('Category deleted successfully');
                    this.loadCategories(); // Reload categories after deletion
                },
                error => {
                    console.error('Error deleting category:', error);
                }
            );
        }
    }

    public navigateToAddCategory(): void {
        console.log('navigateToAddCategory')
        this.router.navigate(['/reports/categories/add']);
    }

}
