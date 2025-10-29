import React from "react";
import { View, Text, Image, StyleSheet, TouchableOpacity} from 'react-native';
import { useLocalSearchParams, router } from 'expo-router';
import { Stack } from "expo-router";

export default function ResultPage(){
    const { photoUri, prediction } = useLocalSearchParams <{ photoUri: string; prediction: string}>();

  return (
    <>
      <Stack.Screen options={{ headerShown: false }} />
      <View style={styles.container}>
        <Text style={styles.title}>Prediction Result</Text>
  
        {photoUri && (
          <Image source={{ uri: photoUri }} style={{ height: 400, width: 400 }} />
        )}
  
        <Text style={styles.resultText}>Predicted Disease:</Text>
      
        {prediction === 'Rust' || prediction === 'Powdery' || prediction === 'Leave Spot'? (
          <Text style={styles.diseasePrediction}>{prediction}</Text>
        ) : (
          <Text style={styles.healthPrediction}>{prediction}</Text>
        )}
  
        <TouchableOpacity style={styles.button} onPress={() => router.push('/')}>
          <Text style={styles.buttonText}>Back to Camera</Text>
        </TouchableOpacity>
      </View>
    </>
  );
}

const styles = StyleSheet.create({
  container: { 
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },

  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  resultText: {
    fontSize: 20,
    marginTop: 10,
  },
  diseasePrediction: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#C42B3B',
    marginTop: 10,
  },
  healthPrediction: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#008000',
    marginTop: 10,
  },
  button: {
    backgroundColor: '#008000',
    marginTop: 30,
    paddingHorizontal: 40,
    paddingVertical: 12,
    borderRadius: 10,
  },
  buttonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
});