package com.example.measuredata

import android.util.Log
import androidx.concurrent.futures.await
import androidx.health.services.client.HealthServicesClient
import androidx.health.services.client.MeasureCallback
import androidx.health.services.client.data.Availability
import androidx.health.services.client.data.DataPoint
import androidx.health.services.client.data.DataType
import androidx.health.services.client.data.DataTypeAvailability
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.channels.sendBlocking
import kotlinx.coroutines.flow.callbackFlow
import javax.inject.Inject

class HealthServicesManager @Inject constructor(
    healthServicesClient: HealthServicesClient
) {
    private val measureClient = healthServicesClient.measureClient

    suspend fun hasHeartRateCapability(): Boolean {
        val capabilities = measureClient.capabilities.await()
        return (DataType.HEART_RATE_BPM in capabilities.supportedDataTypesMeasure)
    }

    fun heartRateMeasureFlow() = callbackFlow<MeasureMessage> {
        val callback = object : MeasureCallback {
            override fun onAvailabilityChanged(dataType: DataType, availability: Availability) {
                if (availability is DataTypeAvailability) {
                    sendBlocking(MeasureMessage.MeasureAvailabilty(availability))
                }
            }

            override fun onData(data: List<DataPoint>) {
                sendBlocking(MeasureMessage.MeasureData(data))
            }
        }

        Log.d(TAG, "Registering for data")
        measureClient.registerCallback(DataType.HEART_RATE_BPM, callback)

        awaitClose {
            Log.d(TAG, "Unregistering for data")
            measureClient.unregisterCallback(DataType.HEART_RATE_BPM, callback)
        }
    }
}

sealed class MeasureMessage {
    class MeasureAvailabilty(val availability: DataTypeAvailability) : MeasureMessage()
    class MeasureData(val data: List<DataPoint>): MeasureMessage()
}
