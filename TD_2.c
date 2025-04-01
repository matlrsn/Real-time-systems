#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

// Semaphore declaration
sem_t sem;

// Function for thread to print a message
void* print_message(void* arg) {
    printf("Hello World\n");
    sleep(10);  // Sleep for 10 seconds
    sem_post(&sem);  // Post the semaphore after printing
    return NULL;
}

int main() {
    pthread_t thread1;

    // Initialize semaphore
    sem_init(&sem, 0, 0);  // Semaphore initialized to 0

    // Create a thread to print "Hello World"
    pthread_create(&thread1, NULL, print_message, NULL);

    // Wait for the semaphore to be posted by the first thread
    sem_wait(&sem);
    printf("Goodbye World\n");

    // Wait for thread to finish
    pthread_join(thread1, NULL);

    // Destroy the semaphore
    sem_destroy(&sem);

    return 0;
}

/*
void* thread(void* arg)
{
	printf("\Hello World\n");
}
int main()
{
	pthread_t t1;
	pthread_create(&t1,NULL,thread,NULL);
}
*/

/*
sem_t mutex;
void* thread(void* arg)
{
	//wait
	sem_wait(&mutex);
	printf("\nEntered thread\n");
	
	//critical section
	sleep(4);
	
	//signal
	printf("\n Exit thread\n");
	sem_post(&mutex);
}
int main()
{
	sem_init(&mutex, 0, 1);
	pthread_t t1,t2;
	pthread_create(&t1,NULL,thread,NULL);
	sleep(2);
	pthread_create(&t2,NULL,thread,NULL);
	pthread_join(t1,NULL);
	pthread_join(t2,NULL);
	sem_destroy(&mutex);
	return 0;
}