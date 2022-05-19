// Generated by Dagger (https://dagger.dev).
package com.example.measuredata;

import dagger.internal.DaggerGenerated;
import dagger.internal.Factory;
import javax.inject.Provider;

@DaggerGenerated
@SuppressWarnings({
    "unchecked",
    "rawtypes"
})
public final class MainViewModel_Factory implements Factory<MainViewModel> {
  private final Provider<HealthServicesManager> healthServicesManagerProvider;

  public MainViewModel_Factory(Provider<HealthServicesManager> healthServicesManagerProvider) {
    this.healthServicesManagerProvider = healthServicesManagerProvider;
  }

  @Override
  public MainViewModel get() {
    return newInstance(healthServicesManagerProvider.get());
  }

  public static MainViewModel_Factory create(
      Provider<HealthServicesManager> healthServicesManagerProvider) {
    return new MainViewModel_Factory(healthServicesManagerProvider);
  }

  public static MainViewModel newInstance(HealthServicesManager healthServicesManager) {
    return new MainViewModel(healthServicesManager);
  }
}
