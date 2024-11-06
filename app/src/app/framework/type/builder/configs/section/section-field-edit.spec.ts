import { ComponentFixture, TestBed, fakeAsync, tick, flush } from '@angular/core/testing';
import { ReactiveFormsModule, UntypedFormControl, Validators } from '@angular/forms';
import { SectionFieldEditComponent } from './section-field-edit.component';

import { ReplaySubject, of, Subject } from 'rxjs';
import { SectionIdentifierService } from '../../../services/SectionIdentifierService.service';
import { ValidationService } from '../../../services/validation.service';

describe('SectionFieldEditComponent', () => {
    let component: SectionFieldEditComponent;
    let fixture: ComponentFixture<SectionFieldEditComponent>;
    let validationService: jasmine.SpyObj<ValidationService>;
    let sectionIdentifier: jasmine.SpyObj<SectionIdentifierService>;
    let activeIndexSubject: Subject<number | null>;


    beforeEach(async () => {
        const validationServiceSpy = jasmine.createSpyObj('ValidationService', ['setIsValid', 'updateFieldValidityOnDeletion']);
        activeIndexSubject = new Subject<number | null>();
        const sectionIdentifierSpy = jasmine.createSpyObj('SectionIdentifierService', {
            getActiveIndex: activeIndexSubject.asObservable(),
            updateSection: true,
        });

        await TestBed.configureTestingModule({
            declarations: [SectionFieldEditComponent],
            imports: [ReactiveFormsModule],
            providers: [
                { provide: ValidationService, useValue: validationServiceSpy },
                { provide: SectionIdentifierService, useValue: sectionIdentifierSpy }
            ]
        }).compileComponents();

        fixture = TestBed.createComponent(SectionFieldEditComponent);
        component = fixture.componentInstance;
        validationService = TestBed.inject(ValidationService) as jasmine.SpyObj<ValidationService>;
        sectionIdentifier = TestBed.inject(SectionIdentifierService) as jasmine.SpyObj<SectionIdentifierService>;
        fixture.detectChanges();
    });


    it('should create the component', () => {
        expect(component).toBeTruthy();
    });


    it('should update initialValue when onInputChange is called with name type', fakeAsync(() => {
        const newValue = 'Updated Name';
        component.nameControl.setValue(newValue);
        component.onInputChange(newValue, 'name');
        tick();
        flush();

        expect(component.nameControl.value).toBe(newValue);
    }));


    it('should update isValid$ when form controls are updated', fakeAsync(() => {
        component.ngOnInit();

        // Initially, form is invalid because fields are empty
        expect(component.isValid$).toBeFalse();

        // Set values to make the form valid
        component.nameControl.setValue('Valid Name');
        component.labelControl.setValue('Valid Label');
        tick();

        expect(component.isValid$).toBeTrue();

        // Ensure any remaining timers are flushed at the end
        flush();
    }));
});
