package com.example.measuredata;

import java.lang.System;

@kotlin.Metadata(mv = {1, 5, 1}, k = 1, d1 = {"\u0000\u0016\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\b6\u0018\u00002\u00020\u0001:\u0002\u0003\u0004B\u0007\b\u0004\u00a2\u0006\u0002\u0010\u0002\u0082\u0001\u0002\u0005\u0006\u00a8\u0006\u0007"}, d2 = {"Lcom/example/measuredata/MeasureMessage;", "", "()V", "MeasureAvailabilty", "MeasureData", "Lcom/example/measuredata/MeasureMessage$MeasureAvailabilty;", "Lcom/example/measuredata/MeasureMessage$MeasureData;", "app_debug"})
public abstract class MeasureMessage {
    
    private MeasureMessage() {
        super();
    }
    
    @kotlin.Metadata(mv = {1, 5, 1}, k = 1, d1 = {"\u0000\u0012\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0004\u0018\u00002\u00020\u0001B\r\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u00a2\u0006\u0002\u0010\u0004R\u0011\u0010\u0002\u001a\u00020\u0003\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0005\u0010\u0006\u00a8\u0006\u0007"}, d2 = {"Lcom/example/measuredata/MeasureMessage$MeasureAvailabilty;", "Lcom/example/measuredata/MeasureMessage;", "availability", "Landroidx/health/services/client/data/DataTypeAvailability;", "(Landroidx/health/services/client/data/DataTypeAvailability;)V", "getAvailability", "()Landroidx/health/services/client/data/DataTypeAvailability;", "app_debug"})
    public static final class MeasureAvailabilty extends com.example.measuredata.MeasureMessage {
        @org.jetbrains.annotations.NotNull()
        private final androidx.health.services.client.data.DataTypeAvailability availability = null;
        
        public MeasureAvailabilty(@org.jetbrains.annotations.NotNull()
        androidx.health.services.client.data.DataTypeAvailability availability) {
            super();
        }
        
        @org.jetbrains.annotations.NotNull()
        public final androidx.health.services.client.data.DataTypeAvailability getAvailability() {
            return null;
        }
    }
    
    @kotlin.Metadata(mv = {1, 5, 1}, k = 1, d1 = {"\u0000\u0016\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0002\b\u0004\u0018\u00002\u00020\u0001B\u0013\u0012\f\u0010\u0002\u001a\b\u0012\u0004\u0012\u00020\u00040\u0003\u00a2\u0006\u0002\u0010\u0005R\u0017\u0010\u0002\u001a\b\u0012\u0004\u0012\u00020\u00040\u0003\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0006\u0010\u0007\u00a8\u0006\b"}, d2 = {"Lcom/example/measuredata/MeasureMessage$MeasureData;", "Lcom/example/measuredata/MeasureMessage;", "data", "", "Landroidx/health/services/client/data/DataPoint;", "(Ljava/util/List;)V", "getData", "()Ljava/util/List;", "app_debug"})
    public static final class MeasureData extends com.example.measuredata.MeasureMessage {
        @org.jetbrains.annotations.NotNull()
        private final java.util.List<androidx.health.services.client.data.DataPoint> data = null;
        
        public MeasureData(@org.jetbrains.annotations.NotNull()
        java.util.List<androidx.health.services.client.data.DataPoint> data) {
            super();
        }
        
        @org.jetbrains.annotations.NotNull()
        public final java.util.List<androidx.health.services.client.data.DataPoint> getData() {
            return null;
        }
    }
}