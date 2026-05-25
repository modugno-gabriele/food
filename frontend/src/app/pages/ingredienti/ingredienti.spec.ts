import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Ingredienti } from './ingredienti';

describe('Ingredienti', () => {
  let component: Ingredienti;
  let fixture: ComponentFixture<Ingredienti>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Ingredienti],
    }).compileComponents();

    fixture = TestBed.createComponent(Ingredienti);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
