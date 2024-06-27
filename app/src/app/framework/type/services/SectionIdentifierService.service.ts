import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

interface Section {
    newValue: string;
    index: number;
}

@Injectable({
    providedIn: 'root',
})
export class SectionIdentifierService {
    private sections: { [initialValue: string]: Section } = {};
    private isIdentifierValidSubject = new BehaviorSubject<boolean>(true);

    constructor() { }


    addSection(initialValue: string, newValue: string, index: number): boolean {
        if (this.sectionExists(newValue)) {
            this.checkGlobalValidity();
            return false;
        }

        // Adjust indices of sections that come after the new section
        for (const section of Object.values(this.sections)) {
            if (section.index >= index) {
                section.index += 1;
            }
        }

        this.sections[initialValue] = { newValue, index };
        this.checkGlobalValidity();
        return true;
    }


    updateSection(initialValue: string, newValue: string): boolean {
        console.log('update section')
        if (!this.sections[initialValue]) {

            this.checkGlobalValidity();
            return false;
        }

        const oldNewValue = this.sections[initialValue].newValue;
        const oldIndex = this.sections[initialValue].index;

        // Temporarily remove the current section to avoid self-comparison
        delete this.sections[initialValue];

        if (this.sectionExists(newValue)) {
            // Re-add the section with the original value

            console.log('update section22')
            // this.sections[initialValue] = { newValue: oldNewValue, index: oldIndex };
            this.sections[initialValue] = { newValue, index: oldIndex };
            this.checkGlobalValidity();
            return false;
        }

        // Re-add the section with the new value
        this.sections[initialValue] = { newValue, index: oldIndex };
        this.checkGlobalValidity();
        return true;
    }


    sectionExists(newValue: string): boolean {
        return Object.values(this.sections).some(section => section.newValue === newValue);
    }


    getSections(): { [initialValue: string]: Section } {
        return this.sections;
    }


    removeSection(index: number): void {
        const sectionEntries = Object.entries(this.sections);
        const sectionToRemove = sectionEntries.find(([_, section]) => section.index === index);

        if (!sectionToRemove) {
            return;
        }

        const [initialValueToRemove] = sectionToRemove;
        delete this.sections[initialValueToRemove];

        // Adjust indexes of remaining sections
        for (const section of Object.values(this.sections)) {
            if (section.index > index) {
                section.index -= 1;
            }
        }

        this.checkGlobalValidity();
    }


    updateSectionIndexes(draggedIndex: number, newIndex: number): void {
        if (Math.abs(draggedIndex - newIndex) === 1 && draggedIndex < newIndex) {
            return;
        }

        if (draggedIndex === newIndex) {
            return;
        }

        if (draggedIndex < newIndex) {
            newIndex -= 1;
        }

        const sectionEntries = Object.entries(this.sections);
        const draggedSectionEntry = sectionEntries.find(([_, section]) => section.index === draggedIndex);

        if (!draggedSectionEntry) {
            return;
        }

        const [draggedInitialValue, draggedSection] = draggedSectionEntry;

        sectionEntries.forEach(([initialValue, section]) => {
            if (draggedIndex < newIndex) {
                if (section.index > draggedIndex && section.index <= newIndex) {
                    section.index -= 1;
                }
            } else if (draggedIndex > newIndex) {
                if (section.index < draggedIndex && section.index >= newIndex) {
                    section.index += 1;
                }
            }
        });

        draggedSection.index = newIndex;

        this.sections = sectionEntries.reduce((acc, [initialValue, section]) => {
            acc[initialValue] = section;
            return acc;
        }, {});

        this.checkGlobalValidity();
    }


    private setIsIdentifierValid(isValid: boolean): void {
        this.isIdentifierValidSubject.next(isValid);
    }


    getIsIdentifierValid(): Observable<boolean> {
        return this.isIdentifierValidSubject.asObservable();
    }


    private checkGlobalValidity(): void {
        const newValues = Object.values(this.sections).map(section => section.newValue);
        const uniqueValues = new Set(newValues);
        const isValid = newValues.length === uniqueValues.size;

        console.log('newValues:', newValues);
        console.log('uniqueValues:', uniqueValues);
        console.log('checkGlobalValidity isValid:', isValid);

        this.setIsIdentifierValid(isValid);
    }

    getDroppedIndex(index?: number): number {
        return index;
    }
}