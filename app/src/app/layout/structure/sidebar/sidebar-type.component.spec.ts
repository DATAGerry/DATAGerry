import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SidebarTypeComponent } from './sidebar-type.component';

import { By } from '@angular/platform-browser';
import { RouterTestingModule } from '@angular/router/testing';
import { CmdbType } from 'src/app/framework/models/cmdb-type';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ObjectService } from 'src/app/framework/services/object.service';
import { SidebarService } from '../../services/sidebar.service';

describe('SidebarTypeComponent', () => {
    let component: SidebarTypeComponent;
    let fixture: ComponentFixture<SidebarTypeComponent>;
    let mockObjectService;
    let mockSidebarService;

    beforeEach(async () => {
        mockObjectService = jasmine.createSpyObj(['someMethod']);
        mockSidebarService = jasmine.createSpyObj(['initializeCounter', 'deleteCounter']);

        await TestBed.configureTestingModule({
            declarations: [SidebarTypeComponent],
            providers: [
                { provide: ObjectService, useValue: mockObjectService },
                { provide: SidebarService, useValue: mockSidebarService }
            ]

        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(SidebarTypeComponent);
        component = fixture.componentInstance;
    });

    it('should create the component', () => {
        expect(component).toBeTruthy();
    });

    it('should initialize counter on init', () => {
        component.ngOnInit();
        expect(mockSidebarService.initializeCounter).toHaveBeenCalledWith(component);
    });

    it('should delete counter on destroy', () => {
        component.ngOnDestroy();
        expect(mockSidebarService.deleteCounter).toHaveBeenCalledWith(component);
    });

    it('should not render if type is not provided', () => {
        component.type = null;
        fixture.detectChanges();
        const listItem = fixture.debugElement.query(By.css('li'));
        expect(listItem).toBeNull();
    });


});
